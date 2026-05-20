"""Smoke tests for the CLI entry point."""

from typer.testing import CliRunner

from remnote2obsidian.cli import app


def test_cli_help_runs() -> None:
    """The Typer CLI should expose help successfully."""
    result = CliRunner().invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "migrate" in result.stdout
