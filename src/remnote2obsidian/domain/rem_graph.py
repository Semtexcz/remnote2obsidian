"""Build preservation-first RemNote graph nodes and relationships."""

from __future__ import annotations

import re
from dataclasses import replace

from remnote2obsidian.domain.rich_text import parse_rich_text_fragments
from remnote2obsidian.models import (
    AttachmentReference,
    AttachmentReferenceKind,
    Diagnostic,
    JsonObject,
    JsonValue,
    RawCardMetadata,
    RawRemDocument,
    RemGraph,
    RemGraphNode,
    Result,
    SourceContext,
)


SUPPORTED_REM_TYPES = frozenset({None, 1, 2, 6})
LOCAL_FILE_PATTERN = re.compile(r"%LOCAL_FILE%[^\s\]\[)('\"<>]+")
REMOTE_URL_PATTERN = re.compile(r"https?://[^\s\]\[)('\"<>]+")


def build_rem_graph(
    raw_rems: tuple[RawRemDocument, ...],
    raw_cards: tuple[RawCardMetadata, ...] = (),
) -> Result[RemGraph]:
    """Build graph nodes, hierarchy, card links, and attachment references."""
    diagnostics: list[Diagnostic] = []
    nodes: dict[str, RemGraphNode] = {}

    for raw_rem in raw_rems:
        if raw_rem.rem_id is None:
            continue

        if raw_rem.rem_id in nodes:
            diagnostics.append(
                Diagnostic.error(
                    code="rem_graph_duplicate_id",
                    message=f"Duplicate RemNote ID was skipped: {raw_rem.rem_id}",
                    source=SourceContext(rem_id=raw_rem.rem_id),
                )
            )
            continue

        node_result = _build_node(raw_rem)
        diagnostics.extend(node_result.diagnostics)
        if node_result.data is not None:
            nodes[raw_rem.rem_id] = node_result.data

    hierarchy_result = _apply_hierarchy(nodes)
    diagnostics.extend(hierarchy_result.diagnostics)
    graph = hierarchy_result.data or RemGraph(nodes=nodes)

    card_result = _apply_cards(graph, raw_cards)
    diagnostics.extend(card_result.diagnostics)
    graph = card_result.data or graph

    attachment_result = _apply_attachments(graph)
    diagnostics.extend(attachment_result.diagnostics)
    graph = attachment_result.data or graph

    return Result(data=graph, diagnostics=tuple(diagnostics))


def parse_raw_card_metadata(cards_envelope: JsonObject | None) -> Result[tuple[RawCardMetadata, ...]]:
    """Parse optional `cards.json` docs entries into raw card metadata."""
    if cards_envelope is None:
        return Result.success(())

    docs = cards_envelope.get("docs")
    if not isinstance(docs, list):
        return Result.failure(
            (
                Diagnostic.error(
                    code="raw_card_docs_not_list",
                    message="cards.json top-level `docs` must be a list before parsing.",
                    source=SourceContext(file_path="cards.json"),
                ),
            )
        )

    cards: list[RawCardMetadata] = []
    diagnostics: list[Diagnostic] = []
    for index, record in enumerate(docs):
        source = SourceContext(file_path=f"cards.json:docs[{index}]")
        if not isinstance(record, dict):
            diagnostics.append(
                Diagnostic.error(
                    code="raw_card_record_not_object",
                    message=f"cards.json docs[{index}] must be a JSON object.",
                    source=source,
                )
            )
            continue

        card = RawCardMetadata.from_json(record)
        if card.rem_id is None:
            diagnostics.append(
                Diagnostic.error(
                    code="raw_card_rem_id_missing",
                    message=f"cards.json docs[{index}] is missing a string `rId`.",
                    source=source,
                )
            )
            continue
        cards.append(card)

    return Result(data=tuple(cards), diagnostics=tuple(diagnostics))


def _build_node(raw_rem: RawRemDocument) -> Result[RemGraphNode]:
    """Build one graph node from a raw RemNote document."""
    diagnostics: list[Diagnostic] = []
    source = SourceContext(rem_id=raw_rem.rem_id)

    key_result = parse_rich_text_fragments(raw_rem.key, source=source)
    value_result = parse_rich_text_fragments(raw_rem.value, source=source)
    diagnostics.extend(key_result.diagnostics)
    diagnostics.extend(value_result.diagnostics)

    if raw_rem.rem_type not in SUPPORTED_REM_TYPES:
        diagnostics.append(
            Diagnostic.warning(
                code="rem_graph_unsupported_type",
                message=f"Unsupported RemNote type was preserved: {raw_rem.rem_type!r}",
                source=source,
            )
        )

    return Result(
        data=RemGraphNode(
            rem_id=raw_rem.rem_id or "",
            raw_rem=raw_rem,
            key_fragments=key_result.data or (),
            value_fragments=value_result.data or (),
            parent_id=raw_rem.parent,
            explicit_child_ids=raw_rem.children,
            sub_block_ids=raw_rem.sub_blocks,
        ),
        diagnostics=tuple(diagnostics),
    )


def _apply_hierarchy(nodes: dict[str, RemGraphNode]) -> Result[RemGraph]:
    """Connect graph nodes through parent, children, and subBlocks fields."""
    diagnostics: list[Diagnostic] = []
    child_ids_by_parent: dict[str, list[str]] = {rem_id: [] for rem_id in nodes}

    for node in nodes.values():
        if node.parent_id is not None:
            if node.parent_id in nodes:
                child_ids_by_parent[node.parent_id].append(node.rem_id)
            else:
                diagnostics.append(
                    Diagnostic.warning(
                        code="rem_graph_missing_parent",
                        message=f"Parent RemNote ID does not exist: {node.parent_id}",
                        source=SourceContext(rem_id=node.rem_id),
                    )
                )

        for child_id in (*node.explicit_child_ids, *node.sub_block_ids):
            if child_id not in nodes:
                diagnostics.append(
                    Diagnostic.warning(
                        code="rem_graph_missing_child",
                        message=f"Child RemNote ID does not exist: {child_id}",
                        source=SourceContext(rem_id=node.rem_id),
                    )
                )

    updated_nodes: dict[str, RemGraphNode] = {}
    for rem_id, node in nodes.items():
        child_ids = _merge_ordered_ids(
            node.explicit_child_ids,
            node.sub_block_ids,
            tuple(child_ids_by_parent[rem_id]),
        )
        updated_nodes[rem_id] = replace(node, child_ids=child_ids)

    root_ids = tuple(
        node.rem_id
        for node in updated_nodes.values()
        if node.parent_id is None or node.parent_id not in updated_nodes
    )

    return Result(data=RemGraph(nodes=updated_nodes, root_ids=root_ids), diagnostics=tuple(diagnostics))


def _apply_cards(graph: RemGraph, raw_cards: tuple[RawCardMetadata, ...]) -> Result[RemGraph]:
    """Attach raw card metadata to matching graph nodes by `rId`."""
    if not raw_cards:
        return Result.success(graph)

    diagnostics: list[Diagnostic] = []
    cards_by_rem_id: dict[str, list[RawCardMetadata]] = {rem_id: [] for rem_id in graph.nodes}
    for card in raw_cards:
        if card.rem_id is None:
            continue
        if card.rem_id not in graph.nodes:
            diagnostics.append(
                Diagnostic.warning(
                    code="rem_graph_card_missing_rem",
                    message=f"Card references a missing RemNote ID: {card.rem_id}",
                    source=SourceContext(rem_id=card.rem_id),
                )
            )
            continue
        cards_by_rem_id[card.rem_id].append(card)

    updated_nodes = {
        rem_id: replace(node, cards=tuple(cards_by_rem_id[rem_id]))
        for rem_id, node in graph.nodes.items()
    }
    return Result(
        data=RemGraph(nodes=updated_nodes, root_ids=graph.root_ids),
        diagnostics=tuple(diagnostics),
    )


def _apply_attachments(graph: RemGraph) -> Result[RemGraph]:
    """Attach discovered local and remote attachment references to graph nodes."""
    updated_nodes: dict[str, RemGraphNode] = {}
    for rem_id, node in graph.nodes.items():
        updated_nodes[rem_id] = replace(
            node,
            attachments=tuple(_extract_attachment_references(rem_id, node.raw_rem.raw)),
        )
    return Result.success(RemGraph(nodes=updated_nodes, root_ids=graph.root_ids))


def _extract_attachment_references(rem_id: str, value: JsonValue) -> tuple[AttachmentReference, ...]:
    """Extract attachment references from raw nested RemNote data."""
    references: list[AttachmentReference] = []
    for source_path, text in _walk_strings(value):
        for match in LOCAL_FILE_PATTERN.finditer(text):
            references.append(
                AttachmentReference(
                    rem_id=rem_id,
                    kind=AttachmentReferenceKind.LOCAL_FILE,
                    value=match.group(0),
                    source_path=source_path,
                )
            )
        for match in REMOTE_URL_PATTERN.finditer(text):
            references.append(
                AttachmentReference(
                    rem_id=rem_id,
                    kind=AttachmentReferenceKind.REMOTE_URL,
                    value=match.group(0),
                    source_path=source_path,
                )
            )
    return tuple(references)


def _walk_strings(value: JsonValue, path: str = "$") -> tuple[tuple[str, str], ...]:
    """Return all strings in a nested JSON value with deterministic source paths."""
    if isinstance(value, str):
        return ((path, value),)
    if isinstance(value, list):
        strings: list[tuple[str, str]] = []
        for index, item in enumerate(value):
            strings.extend(_walk_strings(item, f"{path}[{index}]"))
        return tuple(strings)
    if isinstance(value, dict):
        strings = []
        for key, item in value.items():
            strings.extend(_walk_strings(item, f"{path}.{key}"))
        return tuple(strings)
    return ()


def _merge_ordered_ids(*groups: tuple[str, ...]) -> tuple[str, ...]:
    """Merge ID groups while preserving first-seen order."""
    seen: set[str] = set()
    merged: list[str] = []
    for group in groups:
        for item in group:
            if item in seen:
                continue
            seen.add(item)
            merged.append(item)
    return tuple(merged)
