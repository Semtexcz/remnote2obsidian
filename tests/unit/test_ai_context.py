"""Tests for AI context manifest generation and writing."""

from pathlib import Path

from remnote2obsidian.adapters import AiContextWriter
from remnote2obsidian.domain import (
    build_rem_graph,
    generate_ai_manifest,
    generate_markdown_paths,
    serialize_ai_manifest,
)
from remnote2obsidian.models import AI_CONTEXT_MANIFEST_PATH, RawCardMetadata, RawRemDocument


def test_generate_ai_manifest_serializes_deterministically() -> None:
    """The AI manifest should preserve traceability and serialize deterministically."""
    graph = build_rem_graph(
        (
            RawRemDocument.from_json(
                {
                    "_id": "root",
                    "key": ["Root"],
                    "value": ["See ", {"i": "q", "_id": "child"}],
                    "children": ["child"],
                }
            ),
            RawRemDocument.from_json(
                {
                    "_id": "child",
                    "parent": "root",
                    "key": ["Child"],
                    "value": ["%LOCAL_FILE%fixture.pdf"],
                }
            ),
        ),
        (RawCardMetadata.from_json({"_id": "card-1", "rId": "root"}),),
    ).data
    assert graph is not None
    path_map = generate_markdown_paths(graph).data
    assert path_map is not None

    first_manifest = generate_ai_manifest(graph, path_map).data
    second_manifest = generate_ai_manifest(graph, path_map).data

    assert first_manifest == second_manifest
    assert first_manifest is not None
    assert serialize_ai_manifest(first_manifest) == (
        "{\n"
        "  \"entries\": [\n"
        "    {\n"
        "      \"attachment_count\": 0,\n"
        "      \"card_count\": 1,\n"
        "      \"child_ids\": [\n"
        "        \"child\"\n"
        "      ],\n"
        "      \"markdown_path\": \"notes/root--root.md\",\n"
        "      \"parent_id\": null,\n"
        "      \"reference_ids\": [\n"
        "        \"child\"\n"
        "      ],\n"
        "      \"remnote_id\": \"root\"\n"
        "    },\n"
        "    {\n"
        "      \"attachment_count\": 1,\n"
        "      \"card_count\": 0,\n"
        "      \"child_ids\": [],\n"
        "      \"markdown_path\": \"notes/child--child.md\",\n"
        "      \"parent_id\": \"root\",\n"
        "      \"reference_ids\": [],\n"
        "      \"remnote_id\": \"child\"\n"
        "    }\n"
        "  ],\n"
        "  \"version\": 1\n"
        "}\n"
    )


def test_ai_context_writer_writes_manifest_to_stable_path(tmp_path: Path) -> None:
    """The AI context writer should create the manifest directory and file."""
    graph = build_rem_graph((RawRemDocument.from_json({"_id": "root", "key": ["Root"]}),)).data
    assert graph is not None
    path_map = generate_markdown_paths(graph).data
    assert path_map is not None
    manifest = generate_ai_manifest(graph, path_map).data
    assert manifest is not None

    first_result = AiContextWriter().write_manifest(tmp_path, manifest)
    second_result = AiContextWriter().write_manifest(tmp_path, manifest)

    expected_path = tmp_path / AI_CONTEXT_MANIFEST_PATH
    assert first_result.is_success
    assert second_result.is_success
    assert first_result.data == expected_path
    assert expected_path.read_text(encoding="utf-8") == serialize_ai_manifest(manifest)


def test_ai_context_writer_reports_write_failures(tmp_path: Path) -> None:
    """The AI context writer should report filesystem write failures."""
    blocked_path = tmp_path / ".remnote2obsidian"
    blocked_path.write_text("occupied", encoding="utf-8")
    graph = build_rem_graph((RawRemDocument.from_json({"_id": "root"}),)).data
    assert graph is not None
    path_map = generate_markdown_paths(graph).data
    assert path_map is not None
    manifest = generate_ai_manifest(graph, path_map).data
    assert manifest is not None

    result = AiContextWriter().write_manifest(tmp_path, manifest)

    assert not result.is_success
    assert result.errors[0].code == "ai_context_manifest_write_failed"
    assert blocked_path.read_text(encoding="utf-8") == "occupied"
