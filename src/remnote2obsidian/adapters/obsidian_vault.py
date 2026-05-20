"""Filesystem adapter for writing generated Obsidian vault Markdown files."""

from __future__ import annotations

from pathlib import Path

from remnote2obsidian.models import Diagnostic, MarkdownDocument, Result, SourceContext


class ObsidianVaultWriter:
    """Write generated Markdown documents into an Obsidian-compatible directory."""

    def write_documents(
        self,
        output_directory: Path | str,
        documents: tuple[MarkdownDocument, ...],
    ) -> Result[tuple[Path, ...]]:
        """Write Markdown documents and return written filesystem paths."""
        output_path = Path(output_directory)
        written_paths: list[Path] = []
        diagnostics: list[Diagnostic] = []

        for document in documents:
            destination = output_path / document.relative_path
            source = SourceContext(file_path=str(destination), rem_id=document.rem_id)
            try:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(document.content, encoding="utf-8")
            except OSError as error:
                diagnostics.append(
                    Diagnostic.error(
                        code="obsidian_vault_write_failed",
                        message=f"Could not write Markdown document: {destination}: {error}",
                        source=source,
                    )
                )
                continue
            written_paths.append(destination)

        return Result(data=tuple(written_paths), diagnostics=tuple(diagnostics))
