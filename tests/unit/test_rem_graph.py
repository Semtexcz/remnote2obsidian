"""Tests for RemNote graph construction."""

import json
from pathlib import Path

from remnote2obsidian.domain import build_rem_graph, parse_raw_card_metadata, parse_raw_rem_documents
from remnote2obsidian.models import AttachmentReferenceKind, JsonObject, RawCardMetadata, RawRemDocument


FIXTURES_DIR = Path(__file__).parents[1] / "fixtures"


def test_build_rem_graph_keys_nodes_by_original_remnote_id() -> None:
    """Graph nodes should be keyed by original RemNote IDs and preserve source data."""
    raw_rems = (
        RawRemDocument.from_json(
            {
                "_id": "rem-root",
                "key": ["Root"],
                "children": ["rem-child"],
                "custom": {"preserve": True},
            }
        ),
        RawRemDocument.from_json({"_id": "rem-child", "parent": "rem-root", "key": ["Child"]}),
    )

    result = build_rem_graph(raw_rems)

    assert result.is_success
    assert result.data is not None
    assert tuple(result.data.nodes) == ("rem-root", "rem-child")
    assert result.data.nodes["rem-root"].rem_id == "rem-root"
    assert result.data.nodes["rem-root"].raw_rem.unknown_fields == {"custom": {"preserve": True}}
    assert result.data.nodes["rem-root"].key_fragments[0].text == "Root"


def test_build_rem_graph_reports_duplicate_ids_deterministically() -> None:
    """Duplicate RemNote IDs should produce a stable diagnostic and skip later records."""
    raw_rems = (
        RawRemDocument.from_json({"_id": "duplicate", "key": ["First"]}),
        RawRemDocument.from_json({"_id": "duplicate", "key": ["Second"]}),
    )

    result = build_rem_graph(raw_rems)

    assert not result.is_success
    assert result.data is not None
    assert tuple(result.data.nodes) == ("duplicate",)
    assert result.data.nodes["duplicate"].key_fragments[0].text == "First"
    assert result.errors[0].code == "rem_graph_duplicate_id"
    assert result.errors[0].source is not None
    assert result.errors[0].source.rem_id == "duplicate"


def test_build_rem_graph_reconstructs_hierarchy_and_roots() -> None:
    """Graph hierarchy should combine explicit children and parent fields deterministically."""
    raw_rems = (
        RawRemDocument.from_json({"_id": "root", "children": ["child-a"], "subBlocks": ["sub"]}),
        RawRemDocument.from_json({"_id": "child-a", "parent": "root"}),
        RawRemDocument.from_json({"_id": "child-b", "parent": "root"}),
        RawRemDocument.from_json({"_id": "sub", "parent": "root"}),
    )

    result = build_rem_graph(raw_rems)

    assert result.is_success
    assert result.data is not None
    assert result.data.root_ids == ("root",)
    assert result.data.nodes["root"].child_ids == ("child-a", "sub", "child-b")


def test_build_rem_graph_reports_broken_hierarchy_links() -> None:
    """Missing parent and child IDs should produce source-linked warnings."""
    raw_rems = (
        RawRemDocument.from_json({"_id": "root", "children": ["missing-child"]}),
        RawRemDocument.from_json({"_id": "orphan", "parent": "missing-parent"}),
    )

    result = build_rem_graph(raw_rems)

    assert result.is_success
    assert result.data is not None
    assert result.data.root_ids == ("root", "orphan")
    assert tuple(diagnostic.code for diagnostic in result.warnings) == (
        "rem_graph_missing_child",
        "rem_graph_missing_parent",
    )


def test_build_rem_graph_preserves_and_reports_unknown_types() -> None:
    """Unsupported RemNote type values should stay available on graph nodes."""
    raw_rems = (RawRemDocument.from_json({"_id": "unknown-type", "type": 999}),)

    result = build_rem_graph(raw_rems)

    assert result.is_success
    assert result.data is not None
    assert result.data.nodes["unknown-type"].rem_type == 999
    assert result.warnings[0].code == "rem_graph_unsupported_type"
    assert result.warnings[0].source is not None
    assert result.warnings[0].source.rem_id == "unknown-type"


def test_parse_raw_card_metadata_and_attach_cards_to_graph_nodes() -> None:
    """Cards should attach to matching Rem nodes and preserve unknown metadata."""
    raw_rems = (RawRemDocument.from_json({"_id": "rem-1"}),)
    card_result = parse_raw_card_metadata(
        {
            "docs": [
                {"_id": "card-1", "rId": "rem-1", "ml": "New", "custom": "preserve"},
                {"_id": "card-2", "rId": "rem-1", "c": "f"},
            ]
        }
    )

    assert card_result.is_success
    assert card_result.data is not None
    graph_result = build_rem_graph(raw_rems, card_result.data)

    assert graph_result.is_success
    assert graph_result.data is not None
    cards = graph_result.data.nodes["rem-1"].cards
    assert tuple(card.card_id for card in cards) == ("card-1", "card-2")
    assert cards[0].unknown_fields == {"custom": "preserve"}


def test_missing_cards_json_is_accepted() -> None:
    """Missing optional card data should not block graph construction."""
    raw_rems = (RawRemDocument.from_json({"_id": "rem-1"}),)
    card_result = parse_raw_card_metadata(None)
    graph_result = build_rem_graph(raw_rems, card_result.data or ())

    assert card_result.is_success
    assert graph_result.is_success
    assert graph_result.data is not None
    assert graph_result.data.nodes["rem-1"].cards == ()


def test_unmatched_cards_produce_diagnostics() -> None:
    """Cards whose `rId` is missing from the graph should be reported."""
    raw_cards = (RawCardMetadata.from_json({"_id": "card-1", "rId": "missing-rem"}),)

    result = build_rem_graph((RawRemDocument.from_json({"_id": "rem-1"}),), raw_cards)

    assert result.is_success
    assert result.warnings[0].code == "rem_graph_card_missing_rem"
    assert result.warnings[0].source is not None
    assert result.warnings[0].source.rem_id == "missing-rem"


def test_build_rem_graph_extracts_attachment_references_from_fixture() -> None:
    """Attachment extraction should find local placeholders and remote URLs without network."""
    with (FIXTURES_DIR / "hierarchy_references_attachments" / "rem.json").open(
        encoding="utf-8"
    ) as file:
        rem_envelope: JsonObject = json.load(file)

    raw_result = parse_raw_rem_documents(rem_envelope)
    assert raw_result.data is not None

    graph_result = build_rem_graph(raw_result.data)

    assert graph_result.data is not None
    child_attachments = graph_result.data.nodes["rem-child"].attachments
    reference_attachments = graph_result.data.nodes["rem-reference"].attachments
    assert child_attachments[0].kind == AttachmentReferenceKind.LOCAL_FILE
    assert child_attachments[0].value == "%LOCAL_FILE%fixture-document.pdf"
    assert child_attachments[0].rem_id == "rem-child"
    assert reference_attachments[0].kind == AttachmentReferenceKind.REMOTE_URL
    assert reference_attachments[0].value == "https://remnote-user-data.s3.amazonaws.com/fixture-image.png"
    assert reference_attachments[0].source_path.endswith("imageUrl")
