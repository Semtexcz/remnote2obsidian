"""Integration tests for the migration service."""

from pathlib import Path

from remnote2obsidian.models import MigrationRequest
from remnote2obsidian.services import MigrationService


FIXTURES_DIR = Path(__file__).parents[1] / "fixtures"


def test_migration_service_writes_markdown_and_ai_context(tmp_path: Path) -> None:
    """A small valid export should migrate to Markdown and AI context files."""
    export_dir = FIXTURES_DIR / "valid_with_optional_files"
    output_dir = tmp_path / "vault"
    source_before = {
        path.name: path.read_text(encoding="utf-8") for path in sorted(export_dir.glob("*.json"))
    }

    result = MigrationService().migrate(
        MigrationRequest(export_directory=export_dir, output_directory=output_dir)
    )

    assert result.is_success
    assert result.data is not None
    assert result.data.markdown_document_count == 1
    assert result.data.written_markdown_count == 1
    assert result.data.ai_context_written
    markdown_file = output_dir / "notes/card-source--rem-card-source.md"
    manifest_file = output_dir / ".remnote2obsidian/manifest.json"
    assert markdown_file.exists()
    assert manifest_file.exists()
    assert 'remnote_id: "rem-card-source"' in markdown_file.read_text(encoding="utf-8")
    assert '"remnote_id": "rem-card-source"' in manifest_file.read_text(encoding="utf-8")
    assert source_before == {
        path.name: path.read_text(encoding="utf-8") for path in sorted(export_dir.glob("*.json"))
    }


def test_migration_service_dry_run_does_not_write_output(tmp_path: Path) -> None:
    """Dry-run mode should plan the migration without writing output files."""
    output_dir = tmp_path / "vault"

    result = MigrationService().migrate(
        MigrationRequest(
            export_directory=FIXTURES_DIR / "valid_minimal",
            output_directory=output_dir,
            dry_run=True,
        )
    )

    assert result.is_success
    assert result.data is not None
    assert result.data.dry_run
    assert result.data.markdown_document_count == 1
    assert result.data.written_markdown_count == 0
    assert not result.data.ai_context_written
    assert not output_dir.exists()


def test_migration_service_reports_blocking_errors(tmp_path: Path) -> None:
    """Invalid exports should produce visible blocking errors and no output."""
    output_dir = tmp_path / "vault"

    result = MigrationService().migrate(
        MigrationRequest(export_directory=FIXTURES_DIR / "missing_rem", output_directory=output_dir)
    )

    assert not result.is_success
    assert result.errors[0].code == "json_file_missing"
    assert not output_dir.exists()
