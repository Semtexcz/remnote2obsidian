"""Typer command-line application for RemNote to Obsidian migration."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from remnote2obsidian.cli.reporting import format_migration_report
from remnote2obsidian.models import MigrationRequest
from remnote2obsidian.services import MigrationService


app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def migrate(
    export_directory: Annotated[
        Path,
        typer.Argument(help="Path to the RemNote JSON export directory."),
    ],
    output_directory: Annotated[
        Path,
        typer.Argument(help="Path to the generated Obsidian vault directory."),
    ],
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Validate and plan the migration without writing files."),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Show detailed diagnostics."),
    ] = False,
) -> None:
    """Run the RemNote to Obsidian migration."""
    result = MigrationService().migrate(
        MigrationRequest(
            export_directory=export_directory,
            output_directory=output_directory,
            dry_run=dry_run,
        )
    )
    typer.echo(format_migration_report(result, verbose=verbose))
    if not result.is_success:
        raise typer.Exit(code=1)


def main() -> None:
    """Run the Typer application."""
    app()
