"""Tests for rendering RemNote graph nodes into Markdown."""

from remnote2obsidian.domain import (
    build_rem_graph,
    generate_markdown_paths,
    render_markdown_document,
    render_markdown_documents,
    render_wikilink,
    render_yaml_frontmatter,
)
from remnote2obsidian.models import MarkdownPathMap, RawCardMetadata, RawRemDocument


def test_render_markdown_documents_is_deterministic_and_preserves_content() -> None:
    """Graph nodes should render into stable readable Markdown documents."""
    graph = build_rem_graph(
        (
            RawRemDocument.from_json(
                {
                    "_id": "root-id",
                    "key": ["Root title"],
                    "value": ["Root body"],
                    "children": ["child-id"],
                }
            ),
            RawRemDocument.from_json(
                {
                    "_id": "child-id",
                    "parent": "root-id",
                    "key": ["Child title"],
                    "value": ["Child body"],
                }
            ),
        )
    ).data
    assert graph is not None

    first_result = render_markdown_documents(graph)
    second_result = render_markdown_documents(graph)

    assert first_result.data == second_result.data
    assert first_result.data is not None
    root_document = first_result.data[0]
    assert root_document.relative_path == "notes/root-title--root-id.md"
    assert "# Root title" in root_document.content
    assert "Root body" in root_document.content
    assert "- [[notes/child-title--child-id]]" in root_document.content


def test_render_yaml_frontmatter_is_ordered_and_optional() -> None:
    """Frontmatter should include only available metadata in deterministic order."""
    graph = build_rem_graph(
        (RawRemDocument.from_json({"_id": "rem-1", "parent": "root", "type": 2}),),
        (
            RawCardMetadata.from_json({"_id": "card-1", "rId": "rem-1"}),
            RawCardMetadata.from_json({"_id": "card-2", "rId": "rem-1"}),
        ),
    ).data
    assert graph is not None

    frontmatter = render_yaml_frontmatter(graph.nodes["rem-1"])

    assert frontmatter == (
        "---\n"
        'remnote_id: "rem-1"\n'
        'parent_id: "root"\n'
        "remnote_type: 2\n"
        "card_count: 2\n"
        "card_ids:\n"
        '  - "card-1"\n'
        '  - "card-2"\n'
        "---"
    )


def test_generate_markdown_paths_handles_duplicate_and_empty_titles() -> None:
    """Path generation should avoid collisions with stable RemNote ID suffixes."""
    graph = build_rem_graph(
        (
            RawRemDocument.from_json({"_id": "rem-a", "key": ["Same title"]}),
            RawRemDocument.from_json({"_id": "rem-b", "key": ["Same title"]}),
            RawRemDocument.from_json({"_id": "rem-c"}),
        )
    ).data
    assert graph is not None

    result = generate_markdown_paths(graph)

    assert result.data is not None
    assert result.data.paths_by_rem_id == {
        "rem-a": "notes/same-title--rem-a.md",
        "rem-b": "notes/same-title--rem-b.md",
        "rem-c": "notes/untitled-rem-c--rem-c.md",
    }


def test_render_wikilink_resolves_known_references_and_preserves_unknown_ids() -> None:
    """Wikilinks should resolve through the path map and preserve unresolved IDs."""
    path_map = MarkdownPathMap(paths_by_rem_id={"target": "notes/target-title--target.md"})

    assert render_wikilink("target", path_map) == "[[notes/target-title--target]]"
    assert render_wikilink("missing", path_map) == "[Unresolved RemNote reference: missing]"


def test_render_markdown_document_renders_references_and_unsupported_fragments() -> None:
    """Known references should become wikilinks while unsupported fragments remain visible."""
    graph = build_rem_graph(
        (
            RawRemDocument.from_json(
                {
                    "_id": "source",
                    "key": ["Source"],
                    "value": ["See ", {"i": "q", "_id": "target"}, {"unsupported": True}],
                }
            ),
            RawRemDocument.from_json({"_id": "target", "key": ["Target"]}),
        )
    ).data
    assert graph is not None
    path_map = generate_markdown_paths(graph).data
    assert path_map is not None

    content = render_markdown_document(graph.nodes["source"], path_map)

    assert "See [[notes/target--target]]" in content
    assert "`Unsupported RemNote fragment: {\"unsupported\":true}`" in content
