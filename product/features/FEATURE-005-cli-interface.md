---
feature: FEATURE-005
title: "CLI interface"
status: planned
created: 2026-05-20
---

# CLI interface

## Goal

Provide a thin command-line interface for running the RemNote to Obsidian migration with explicit input and output paths, dry-run support, and verbose reporting.

## Problem

The migration needs a repeatable user-facing entry point that can orchestrate loading, graph parsing, Markdown generation, and AI-context generation without placing domain or filesystem logic inside the CLI layer.

## Scope

- define command-line usage for running the migration
- accept an input path pointing to a RemNote export directory
- accept an output path for the generated Obsidian vault
- support dry-run mode that validates and plans migration work without writing output files
- support verbose mode for more detailed progress and validation reporting
- orchestrate existing services for loading, parsing, Markdown generation, AI-context generation, and writing
- return clear success and failure statuses suitable for scripts
- implement CLI commands and argument parsing with Typer

## Out of Scope

- implementing RemNote loading logic inside the CLI
- implementing graph parsing or transformation logic inside the CLI
- implementing Markdown rendering inside the CLI
- implementing AI-context generation inside the CLI
- adding an interactive user interface
- adding synchronization or watch mode

## Success Criteria

- [ ] CLI accepts explicit input and output paths
- [ ] CLI can run the migration workflow through existing services
- [ ] dry-run mode performs validation and planning without writing output files
- [ ] verbose mode reports additional progress and validation details
- [ ] CLI errors are clear and result in non-zero exit statuses
- [ ] CLI remains thin and contains no domain transformation logic
- [ ] repeated runs with identical inputs produce deterministic outputs through the underlying services

## Notes

- relates to PRD-001
- orchestrates FEATURE-001, FEATURE-002, FEATURE-003, and FEATURE-004
- `cli/` should stay thin and delegate workflow coordination to `services/`
- CLI commands must be implemented with Typer
- filesystem and external I/O belong in `adapters/`
- export files must be treated as read-only input
