"""Tests for parsing `rem.json` docs into raw RemNote models."""

import json
from pathlib import Path

from remnote2obsidian.domain import parse_raw_rem_documents
from remnote2obsidian.models import JsonObject


FIXTURES_DIR = Path(__file__).parents[1] / "fixtures"


def test_parse_raw_rem_documents_preserves_ids_order_and_unknown_fields() -> None:
    """Valid docs entries should become raw Rem models in original order."""
    with (FIXTURES_DIR / "hierarchy_references_attachments" / "rem.json").open(
        encoding="utf-8"
    ) as file:
        rem_envelope: JsonObject = json.load(file)

    result = parse_raw_rem_documents(rem_envelope)

    assert result.is_success
    assert result.data is not None
    assert tuple(raw_rem.rem_id for raw_rem in result.data) == (
        "rem-root",
        "rem-child",
        "rem-grandchild",
        "rem-reference",
    )
    assert result.data[0].unknown_fields == {"fixtureUnknownRootField": {"preserve": True}}
    assert result.data[1].parent == "rem-root"
    assert result.data[2].references == ["rem-reference"]


def test_parse_raw_rem_documents_reports_missing_ids_and_keeps_valid_records() -> None:
    """Records without string IDs should produce diagnostics without stopping parsing."""
    result = parse_raw_rem_documents(
        {
            "docs": [
                {"_id": "rem-valid", "key": ["Valid"]},
                {"key": ["Missing ID"]},
                {"_id": 123, "key": ["Invalid ID type"]},
            ]
        }
    )

    assert not result.is_success
    assert result.data is not None
    assert tuple(raw_rem.rem_id for raw_rem in result.data) == ("rem-valid",)
    assert tuple(diagnostic.code for diagnostic in result.errors) == (
        "raw_rem_id_missing",
        "raw_rem_id_missing",
    )
    assert result.errors[0].source is not None
    assert result.errors[0].source.file_path == "rem.json:docs[1]"


def test_parse_raw_rem_documents_reports_non_object_records_deterministically() -> None:
    """Non-object docs entries should be reported with stable source context."""
    result = parse_raw_rem_documents({"docs": ["not-an-object", {"_id": "rem-valid"}]})

    assert not result.is_success
    assert result.data is not None
    assert tuple(raw_rem.rem_id for raw_rem in result.data) == ("rem-valid",)
    assert result.errors[0].code == "raw_rem_record_not_object"
    assert result.errors[0].source is not None
    assert result.errors[0].source.file_path == "rem.json:docs[0]"


def test_parse_raw_rem_documents_reports_non_list_docs() -> None:
    """The parser should report incompatible docs containers."""
    result = parse_raw_rem_documents({"docs": {"not": "a-list"}})

    assert not result.is_success
    assert result.data is None
    assert result.errors[0].code == "raw_rem_docs_not_list"
