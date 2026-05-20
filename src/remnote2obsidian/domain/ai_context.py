"""Generate deterministic AI context metadata from graph and path data."""

from __future__ import annotations

import json

from remnote2obsidian.models import (
    AiManifest,
    AiManifestEntry,
    MarkdownPathMap,
    RemGraph,
    RemGraphNode,
    Result,
    RichTextFragmentKind,
)


def generate_ai_manifest(graph: RemGraph, path_map: MarkdownPathMap) -> Result[AiManifest]:
    """Generate an AI manifest for graph navigation and source traceability."""
    entries = tuple(
        AiManifestEntry(
            remnote_id=rem_id,
            markdown_path=path_map.paths_by_rem_id[rem_id],
            parent_id=node.parent_id,
            child_ids=node.child_ids,
            reference_ids=_reference_ids(node),
            attachment_count=len(node.attachments),
            card_count=len(node.cards),
        )
        for rem_id, node in graph.nodes.items()
        if rem_id in path_map.paths_by_rem_id
    )
    return Result.success(AiManifest(entries=entries))


def serialize_ai_manifest(manifest: AiManifest) -> str:
    """Serialize an AI manifest as deterministic pretty JSON."""
    return json.dumps(
        manifest.to_json_dict(),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def _reference_ids(node: RemGraphNode) -> tuple[str, ...]:
    """Return unique RemNote reference target IDs from parsed node content."""
    seen: set[str] = set()
    reference_ids: list[str] = []
    for fragment in (*node.key_fragments, *node.value_fragments):
        if fragment.kind != RichTextFragmentKind.REFERENCE or fragment.target_rem_id is None:
            continue
        if fragment.target_rem_id in seen:
            continue
        seen.add(fragment.target_rem_id)
        reference_ids.append(fragment.target_rem_id)
    return tuple(reference_ids)
