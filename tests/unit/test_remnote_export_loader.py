"""Tests for loading raw RemNote export directories."""

from __future__ import annotations

from pathlib import Path
from typing import cast

from remnote2obsidian.adapters import RemNoteExportLoader
from remnote2obsidian.models import JsonArray, JsonObject, RemNoteExport


FIXTURES_DIR = Path(__file__).parents[1] / "fixtures"


def test_loader_reads_valid_fixture_with_only_rem_json() -> None:
    """The loader should load a minimal export containing only `rem.json`."""
    result = RemNoteExportLoader().load(FIXTURES_DIR / "valid_minimal")

    assert result.is_success
    assert isinstance(result.data, RemNoteExport)
    assert set(result.data.files) == {"rem.json"}
    assert result.data.rem == {
        "userId": "user-fixture",
        "knowledgebaseId": "kb-fixture",
        "name": "Minimal Fixture",
        "exportDate": "2026-05-20T00:00:00.000Z",
        "exportVersion": 2,
        "docs": [{"_id": "rem-root", "key": ["Root"], "children": []}],
    }


def test_loader_reads_present_optional_files_deterministically() -> None:
    """The loader should read supported optional files when they are present."""
    result = RemNoteExportLoader().load(FIXTURES_DIR / "valid_with_optional_files")

    assert result.is_success
    assert isinstance(result.data, RemNoteExport)
    assert tuple(result.data.files) == ("rem.json", "cards.json", "metadata.json")
    assert result.data.files["cards.json"] == {
        "userId": "user-fixture",
        "knowledgebaseId": "kb-fixture",
        "name": "Optional Files Fixture Cards",
        "exportDate": "2026-05-20T00:00:00.000Z",
        "exportVersion": 2,
        "docs": [{"_id": "card-1", "rId": "rem-card-source", "ml": "New"}],
    }


def test_loader_reports_missing_required_rem_json() -> None:
    """The loader should report a missing required `rem.json` file."""
    result = RemNoteExportLoader().load(FIXTURES_DIR / "missing_rem")

    assert not result.is_success
    assert isinstance(result.data, RemNoteExport)
    assert set(result.data.files) == {"metadata.json"}
    assert result.errors[0].code == "json_file_missing"


def test_loader_preserves_raw_unknown_fields() -> None:
    """The loader should preserve unknown fields without transformation."""
    result = RemNoteExportLoader().load(FIXTURES_DIR / "hierarchy_references_attachments")

    assert result.is_success
    assert isinstance(result.data, RemNoteExport)
    rem_data = result.data.files["rem.json"]

    assert isinstance(rem_data, dict)
    docs = cast(JsonArray, rem_data["docs"])
    first_doc = cast(JsonObject, docs[0])
    assert first_doc["fixtureUnknownRootField"] == {"preserve": True}
