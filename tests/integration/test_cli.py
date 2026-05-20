"""Integration tests for the Typer CLI."""

from pathlib import Path

from typer.testing import CliRunner

from remnote2obsidian.cli import app


FIXTURES_DIR = Path(__file__).parents[1] / "fixtures"


def test_cli_migrate_success_and_deterministic_rerun(tmp_path: Path) -> None:
    """The CLI should run a full migration and produce deterministic output."""
    output_dir = tmp_path / "vault"
    runner = CliRunner()

    first = runner.invoke(app, [str(FIXTURES_DIR / "valid_minimal"), str(output_dir)])
    first_markdown = (output_dir / "notes/root--rem-root.md").read_text(encoding="utf-8")
    first_manifest = (output_dir / ".remnote2obsidian/manifest.json").read_text(encoding="utf-8")
    second = runner.invoke(app, [str(FIXTURES_DIR / "valid_minimal"), str(output_dir)])

    assert first.exit_code == 0
    assert second.exit_code == 0
    assert "Migration succeeded." in first.stdout
    assert (output_dir / "notes/root--rem-root.md").read_text(encoding="utf-8") == first_markdown
    assert (
        output_dir / ".remnote2obsidian/manifest.json"
    ).read_text(encoding="utf-8") == first_manifest


def test_cli_migrate_dry_run_and_verbose_output(tmp_path: Path) -> None:
    """The CLI should support dry-run and verbose reporting."""
    output_dir = tmp_path / "vault"

    result = CliRunner().invoke(
        app,
        [
            str(FIXTURES_DIR / "valid_minimal"),
            str(output_dir),
            "--dry-run",
            "--verbose",
        ],
    )

    assert result.exit_code == 0
    assert "Dry run: yes" in result.stdout
    assert "Planned output files: 2" in result.stdout
    assert not output_dir.exists()


def test_cli_migrate_failure_exit_status(tmp_path: Path) -> None:
    """The CLI should return a non-zero exit status for blocking failures."""
    result = CliRunner().invoke(
        app,
        [str(FIXTURES_DIR / "missing_rem"), str(tmp_path / "vault")],
    )

    assert result.exit_code == 1
    assert "Migration failed." in result.stdout
    assert "ERROR json_file_missing" in result.stdout
