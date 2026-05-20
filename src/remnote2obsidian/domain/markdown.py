"""Render RemNote graph nodes into deterministic Markdown documents."""

from __future__ import annotations

import json
import re

from remnote2obsidian.models import (
    MarkdownDocument,
    MarkdownPathMap,
    RemGraph,
    RemGraphNode,
    Result,
    RichTextFragment,
    RichTextFragmentKind,
)


PATH_SAFE_PATTERN = re.compile(r"[^a-z0-9_-]+")


def generate_markdown_paths(graph: RemGraph) -> Result[MarkdownPathMap]:
    """Generate stable vault-relative Markdown paths for every graph node."""
    paths_by_rem_id = {
        rem_id: f"notes/{_slugify(_node_title(node))}--{_safe_id(rem_id)}.md"
        for rem_id, node in graph.nodes.items()
    }
    return Result.success(MarkdownPathMap(paths_by_rem_id=paths_by_rem_id))


def render_markdown_documents(graph: RemGraph) -> Result[tuple[MarkdownDocument, ...]]:
    """Render all graph nodes into Markdown documents."""
    path_result = generate_markdown_paths(graph)
    path_map = path_result.data or MarkdownPathMap(paths_by_rem_id={})
    documents = tuple(
        MarkdownDocument(
            rem_id=rem_id,
            relative_path=path_map.paths_by_rem_id[rem_id],
            content=render_markdown_document(node, path_map),
        )
        for rem_id, node in graph.nodes.items()
    )
    return Result(data=documents, diagnostics=path_result.diagnostics)


def render_markdown_document(node: RemGraphNode, path_map: MarkdownPathMap) -> str:
    """Render a single graph node as Markdown content."""
    title = _node_title(node)
    parts = [
        render_yaml_frontmatter(node),
        f"# {title}",
    ]

    body = _render_fragments(node.value_fragments, path_map)
    if body:
        parts.append(body)

    if node.child_ids:
        child_lines = ["## Children"]
        child_lines.extend(f"- {render_wikilink(child_id, path_map)}" for child_id in node.child_ids)
        parts.append("\n".join(child_lines))

    if node.attachments:
        attachment_lines = ["## Attachments"]
        attachment_lines.extend(f"- `{attachment.value}`" for attachment in node.attachments)
        parts.append("\n".join(attachment_lines))

    return "\n\n".join(parts).rstrip() + "\n"


def render_yaml_frontmatter(node: RemGraphNode) -> str:
    """Render deterministic YAML frontmatter for a graph node."""
    lines = [
        "---",
        f"remnote_id: {_yaml_scalar(node.rem_id)}",
    ]
    if node.parent_id is not None:
        lines.append(f"parent_id: {_yaml_scalar(node.parent_id)}")
    if node.rem_type is not None:
        lines.append(f"remnote_type: {_yaml_scalar(node.rem_type)}")
    if node.cards:
        lines.append(f"card_count: {len(node.cards)}")
        card_ids = [card.card_id for card in node.cards if card.card_id is not None]
        if card_ids:
            lines.append("card_ids:")
            lines.extend(f"  - {_yaml_scalar(card_id)}" for card_id in card_ids)
    if node.attachments:
        lines.append(f"attachment_count: {len(node.attachments)}")
    lines.append("---")
    return "\n".join(lines)


def render_wikilink(rem_id: str, path_map: MarkdownPathMap) -> str:
    """Render a RemNote reference as an Obsidian wikilink or unresolved fallback."""
    target_path = path_map.path_for_rem(rem_id)
    if target_path is None:
        return f"[Unresolved RemNote reference: {rem_id}]"
    return f"[[{target_path.removesuffix('.md')}]]"


def _render_fragments(fragments: tuple[RichTextFragment, ...], path_map: MarkdownPathMap) -> str:
    """Render parsed rich text fragments into Markdown text."""
    rendered = []
    for fragment in fragments:
        if fragment.kind == RichTextFragmentKind.TEXT and fragment.text is not None:
            rendered.append(fragment.text)
        elif fragment.kind == RichTextFragmentKind.REFERENCE and fragment.target_rem_id is not None:
            rendered.append(render_wikilink(fragment.target_rem_id, path_map))
        else:
            rendered.append(f"`Unsupported RemNote fragment: {_stable_json(fragment.raw)}`")
    return "".join(rendered).strip()


def _node_title(node: RemGraphNode) -> str:
    """Return a readable title for a graph node."""
    title = _render_fragments(node.key_fragments, MarkdownPathMap(paths_by_rem_id={})).strip()
    if title:
        return title
    return f"Untitled {node.rem_id}"


def _slugify(value: str) -> str:
    """Return a deterministic filesystem-safe slug."""
    slug = PATH_SAFE_PATTERN.sub("-", value.casefold()).strip("-")
    return slug or "untitled"


def _safe_id(rem_id: str) -> str:
    """Return a filesystem-safe RemNote ID suffix."""
    return PATH_SAFE_PATTERN.sub("-", rem_id.casefold()).strip("-") or "unknown-id"


def _yaml_scalar(value: object) -> str:
    """Serialize a minimal YAML scalar deterministically."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int | float):
        return str(value)
    if value is None:
        return "null"
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _stable_json(value: object) -> str:
    """Serialize fallback data in a stable compact form."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
