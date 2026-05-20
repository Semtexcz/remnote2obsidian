"""Tests for deterministic CLI migration reporting."""

from remnote2obsidian.cli.reporting import format_migration_report
from remnote2obsidian.models import Diagnostic, MigrationSummary, Result


def test_normal_report_shows_summary_without_warning_details() -> None:
    """Normal reporting should stay concise for successful runs."""
    result = Result.success(
        MigrationSummary(
            dry_run=False,
            loaded_file_count=2,
            rem_count=3,
            graph_node_count=3,
            markdown_document_count=3,
            written_markdown_count=3,
            ai_context_written=True,
        ),
        diagnostics=(Diagnostic.warning("warn", "Useful warning."),),
    )

    assert format_migration_report(result) == (
        "Migration succeeded.\n"
        "Dry run: no\n"
        "Loaded files: 2\n"
        "Raw Rem records: 3\n"
        "Graph nodes: 3\n"
        "Markdown documents: 3\n"
        "Planned output files: 4\n"
        "Written Markdown files: 3\n"
        "AI context written: yes\n"
        "Warnings: 1\n"
        "Errors: 0"
    )


def test_verbose_report_includes_diagnostics_in_order() -> None:
    """Verbose reporting should include source-linked diagnostics deterministically."""
    diagnostics = (
        Diagnostic.warning("first", "First warning."),
        Diagnostic.error("second", "Second error."),
    )
    result: Result[MigrationSummary] = Result(
        data=MigrationSummary(dry_run=True),
        diagnostics=diagnostics,
    )

    report = format_migration_report(result, verbose=True)

    assert report.endswith(
        "Warnings: 1\n"
        "Errors: 1\n"
        "WARNING first: First warning.\n"
        "ERROR second: Second error."
    )
