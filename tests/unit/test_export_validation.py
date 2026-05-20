"""Tests for RemNote export envelope validation."""

from typing import cast

from remnote2obsidian.domain import validate_export_envelope
from remnote2obsidian.models import JsonObject, RemNoteExport


def test_valid_shared_envelopes_and_metadata_pass_validation() -> None:
    """Valid shared envelopes and metadata should pass validation."""
    export = RemNoteExport(
        files={
            "rem.json": {"docs": [], "unknown": {"preserve": True}},
            "cards.json": {"docs": []},
            "metadata.json": {"version": "1.25.19", "device": {"platform": "test"}},
        }
    )

    result = validate_export_envelope(export)

    assert result.is_success
    assert result.data is export
    rem_data = cast(JsonObject, result.data.files["rem.json"])
    assert rem_data["unknown"] == {"preserve": True}


def test_missing_docs_in_shared_envelope_is_reported() -> None:
    """Shared-envelope files should report missing top-level `docs`."""
    export = RemNoteExport(files={"rem.json": {"exportVersion": 2}})

    result = validate_export_envelope(export)

    assert not result.is_success
    assert result.errors[0].code == "export_envelope_docs_missing"
    assert result.errors[0].source is not None
    assert result.errors[0].source.file_path == "rem.json"


def test_non_list_docs_in_shared_envelope_is_reported() -> None:
    """Shared-envelope files should report non-list top-level `docs` values."""
    export = RemNoteExport(files={"rem.json": {"docs": {"not": "a-list"}}})

    result = validate_export_envelope(export)

    assert not result.is_success
    assert result.errors[0].code == "export_envelope_docs_not_list"


def test_metadata_json_does_not_require_docs() -> None:
    """The documented metadata envelope should not require a `docs` list."""
    export = RemNoteExport(files={"metadata.json": {"version": "1.25.19"}})

    result = validate_export_envelope(export)

    assert result.is_success


def test_non_object_metadata_is_reported() -> None:
    """Metadata should still be a top-level JSON object."""
    export = RemNoteExport(files={"metadata.json": []})

    result = validate_export_envelope(export)

    assert not result.is_success
    assert result.errors[0].code == "metadata_envelope_not_object"
