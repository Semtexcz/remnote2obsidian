"""Tests documenting deterministic RemNote export fixtures."""

from __future__ import annotations

import json
from pathlib import Path


FIXTURES_DIR = Path(__file__).parents[1] / "fixtures"


def test_valid_fixture_json_files_are_parseable() -> None:
    """Valid fixture JSON files should parse as deterministic test data."""
    valid_files = (
        FIXTURES_DIR / "valid_minimal" / "rem.json",
        FIXTURES_DIR / "valid_with_optional_files" / "rem.json",
        FIXTURES_DIR / "valid_with_optional_files" / "cards.json",
        FIXTURES_DIR / "valid_with_optional_files" / "metadata.json",
        FIXTURES_DIR / "missing_rem" / "metadata.json",
        FIXTURES_DIR / "hierarchy_references_attachments" / "rem.json",
    )

    for fixture_file in valid_files:
        with fixture_file.open(encoding="utf-8") as file:
            assert json.load(file)


def test_minimal_valid_fixture_contains_required_export_envelope() -> None:
    """The minimal fixture should contain the expected RemNote export envelope."""
    with (FIXTURES_DIR / "valid_minimal" / "rem.json").open(encoding="utf-8") as file:
        export = json.load(file)

    assert export["exportVersion"] == 2
    assert isinstance(export["docs"], list)
    assert export["docs"][0]["_id"] == "rem-root"


def test_invalid_json_fixture_is_intentionally_malformed() -> None:
    """The invalid JSON fixture should remain malformed for loader tests."""
    fixture_file = FIXTURES_DIR / "invalid_json" / "rem.json"

    with fixture_file.open(encoding="utf-8") as file:
        try:
            json.load(file)
        except json.JSONDecodeError:
            return

    raise AssertionError("invalid_json/rem.json should be malformed")


def test_missing_rem_fixture_does_not_contain_required_rem_file() -> None:
    """The missing-rem fixture should omit rem.json while keeping optional files."""
    fixture_dir = FIXTURES_DIR / "missing_rem"

    assert not (fixture_dir / "rem.json").exists()
    assert (fixture_dir / "metadata.json").exists()
