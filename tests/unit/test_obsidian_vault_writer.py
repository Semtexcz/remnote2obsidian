"""Tests for writing generated Markdown files to an Obsidian vault directory."""

from pathlib import Path

from remnote2obsidian.adapters import ObsidianVaultWriter
from remnote2obsidian.models import MarkdownDocument


def test_obsidian_vault_writer_writes_documents_and_directories(tmp_path: Path) -> None:
    """The writer should create directories and write deterministic Markdown content."""
    documents = (
        MarkdownDocument(
            rem_id="rem-1",
            relative_path="notes/root.md",
            content="# Root\n",
        ),
        MarkdownDocument(
            rem_id="rem-2",
            relative_path="notes/nested/child.md",
            content="# Child\n",
        ),
    )

    first_result = ObsidianVaultWriter().write_documents(tmp_path, documents)
    second_result = ObsidianVaultWriter().write_documents(tmp_path, documents)

    assert first_result.is_success
    assert second_result.is_success
    assert (tmp_path / "notes/root.md").read_text(encoding="utf-8") == "# Root\n"
    assert (tmp_path / "notes/nested/child.md").read_text(encoding="utf-8") == "# Child\n"
    assert first_result.data == (
        tmp_path / "notes/root.md",
        tmp_path / "notes/nested/child.md",
    )


def test_obsidian_vault_writer_reports_write_failures(tmp_path: Path) -> None:
    """The writer should report filesystem write failures through diagnostics."""
    output_file = tmp_path / "not-a-directory"
    output_file.write_text("occupied", encoding="utf-8")
    documents = (
        MarkdownDocument(
            rem_id="rem-1",
            relative_path="notes/root.md",
            content="# Root\n",
        ),
    )

    result = ObsidianVaultWriter().write_documents(output_file, documents)

    assert not result.is_success
    assert result.errors[0].code == "obsidian_vault_write_failed"
    assert output_file.read_text(encoding="utf-8") == "occupied"
