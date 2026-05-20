"""Opt-in smoke test for the local large RemNote export."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from remnote2obsidian.adapters import RemNoteExportLoader
from remnote2obsidian.domain import (
    build_rem_graph,
    parse_raw_card_metadata,
    parse_raw_rem_documents,
    validate_export_envelope,
)
from remnote2obsidian.models import JsonObject


LARGE_EXPORT_DIR = Path("data/remnote_full_export")
RUN_LARGE_EXPORT_ENV = "REMNOTE2OBSIDIAN_RUN_LARGE_EXPORT"

pytestmark = pytest.mark.large_export


@pytest.mark.skipif(
    os.environ.get(RUN_LARGE_EXPORT_ENV) != "1",
    reason=f"set {RUN_LARGE_EXPORT_ENV}=1 to run the large export smoke test",
)
def test_large_export_loads_and_builds_graph_without_writing_output() -> None:
    """The real export should load, validate, parse, and build a graph when opted in."""
    if not LARGE_EXPORT_DIR.exists():
        pytest.skip("local large RemNote export is not available")

    load_result = RemNoteExportLoader().load(LARGE_EXPORT_DIR)

    assert load_result.is_success
    assert load_result.data is not None
    validation_result = validate_export_envelope(load_result.data)
    assert validation_result.is_success

    rem_data = load_result.data.files["rem.json"]
    assert isinstance(rem_data, dict)
    rem_parse_result = parse_raw_rem_documents(rem_data)
    assert rem_parse_result.is_success
    assert rem_parse_result.data is not None
    assert len(rem_parse_result.data) > 0

    cards_data = load_result.data.files.get("cards.json")
    card_parse_result = parse_raw_card_metadata(_optional_object(cards_data))
    assert card_parse_result.is_success

    graph_result = build_rem_graph(rem_parse_result.data, card_parse_result.data or ())

    assert graph_result.data is not None
    assert len(graph_result.data.nodes) == len(rem_parse_result.data)


def _optional_object(value: object) -> JsonObject | None:
    """Return a JSON object for optional loaded data."""
    if isinstance(value, dict):
        return value
    return None
