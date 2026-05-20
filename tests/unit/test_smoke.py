"""Smoke tests for the generated CLI entry point."""

from typing import Any

from pytest import CaptureFixture

from remnote2obsidian.main import main


def test_main_runs(capsys: CaptureFixture[Any]) -> None:
    """The starter CLI should execute without errors."""
    main()
    captured = capsys.readouterr()
    assert "Remnote2Obsidian running" in captured.out
