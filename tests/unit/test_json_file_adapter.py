"""Tests for the read-only JSON file adapter."""

from __future__ import annotations

import json
from pathlib import Path

from remnote2obsidian.adapters import JsonFileAdapter


def test_json_file_adapter_reads_valid_json(tmp_path: Path) -> None:
    """The adapter should return parsed JSON without modifying the file."""
    file_path = tmp_path / "data.json"
    file_path.write_text('{"name": "fixture", "items": [1, 2]}', encoding="utf-8")
    original_content = file_path.read_text(encoding="utf-8")

    result = JsonFileAdapter().read(file_path)

    assert result.is_success
    assert result.data == {"name": "fixture", "items": [1, 2]}
    assert file_path.read_text(encoding="utf-8") == original_content


def test_json_file_adapter_reports_missing_files(tmp_path: Path) -> None:
    """The adapter should report missing JSON files as diagnostics."""
    result = JsonFileAdapter().read(tmp_path / "missing.json")

    assert not result.is_success
    assert result.errors[0].code == "json_file_missing"


def test_json_file_adapter_reports_invalid_json(tmp_path: Path) -> None:
    """The adapter should report invalid JSON as a diagnostic."""
    file_path = tmp_path / "broken.json"
    file_path.write_text('{"broken": true', encoding="utf-8")

    result = JsonFileAdapter().read(file_path)

    assert not result.is_success
    assert result.errors[0].code == "json_file_invalid"


def test_json_file_adapter_reports_unreadable_paths(tmp_path: Path) -> None:
    """The adapter should report paths that cannot be read as JSON files."""
    result = JsonFileAdapter().read(tmp_path)

    assert not result.is_success
    assert result.errors[0].code == "json_file_unreadable"


def test_invalid_json_fixture_produces_diagnostic() -> None:
    """The invalid RemNote fixture should produce a JSON diagnostic."""
    fixture_path = Path("tests/fixtures/invalid_json/rem.json")

    result = JsonFileAdapter().read(fixture_path)

    assert not result.is_success
    assert result.errors[0].code == "json_file_invalid"


def test_json_file_adapter_matches_standard_library_parsing(tmp_path: Path) -> None:
    """The adapter should preserve JSON data exactly as standard parsing returns it."""
    file_path = tmp_path / "nested.json"
    file_path.write_text(
        json.dumps({"unknown": {"nested": [True, None, "value"]}}, sort_keys=True),
        encoding="utf-8",
    )

    result = JsonFileAdapter().read(file_path)

    assert result.data == {"unknown": {"nested": [True, None, "value"]}}
