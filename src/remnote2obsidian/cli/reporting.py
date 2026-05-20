"""Deterministic CLI reporting for migration results."""

from __future__ import annotations

from remnote2obsidian.models import Diagnostic, Result
from remnote2obsidian.models.migration import MigrationSummary


def format_migration_report(result: Result[MigrationSummary], *, verbose: bool = False) -> str:
    """Format a migration result for normal or verbose CLI output."""
    summary = result.data
    lines = [f"Migration {'succeeded' if result.is_success else 'failed'}."]

    if summary is not None:
        lines.extend(
            [
                f"Dry run: {'yes' if summary.dry_run else 'no'}",
                f"Loaded files: {summary.loaded_file_count}",
                f"Raw Rem records: {summary.rem_count}",
                f"Graph nodes: {summary.graph_node_count}",
                f"Markdown documents: {summary.markdown_document_count}",
                f"Planned output files: {summary.planned_output_count}",
                f"Written Markdown files: {summary.written_markdown_count}",
                f"AI context written: {'yes' if summary.ai_context_written else 'no'}",
            ]
        )

    lines.append(f"Warnings: {len(result.warnings)}")
    lines.append(f"Errors: {len(result.errors)}")

    if verbose or result.errors:
        lines.extend(_format_diagnostics(result.diagnostics))

    return "\n".join(lines)


def _format_diagnostics(diagnostics: tuple[Diagnostic, ...]) -> list[str]:
    """Format diagnostics in their deterministic source order."""
    return [format_diagnostic(diagnostic) for diagnostic in diagnostics]


def format_diagnostic(diagnostic: Diagnostic) -> str:
    """Format one diagnostic for CLI output."""
    source_parts: list[str] = []
    if diagnostic.source is not None:
        if diagnostic.source.file_path is not None:
            source_parts.append(f"file={diagnostic.source.file_path}")
        if diagnostic.source.rem_id is not None:
            source_parts.append(f"rem={diagnostic.source.rem_id}")

    source = f" ({', '.join(source_parts)})" if source_parts else ""
    return f"{diagnostic.severity.upper()} {diagnostic.code}: {diagnostic.message}{source}"
