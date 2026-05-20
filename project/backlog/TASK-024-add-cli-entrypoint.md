---
task: TASK-024
title: "Add CLI entrypoint"
status: backlog
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-005
  - US-001
  - US-013
---

# Add CLI entrypoint

## Goal

Implement the command-line interface for running the migration service. The CLI should accept input and output paths plus dry-run and verbose flags.

## Context

The CLI must stay thin and must not contain domain parsing, rendering, or filesystem logic beyond argument handling and user-facing reporting.

## Touchpoints

- `src/remnote2obsidian/main.py`
- `src/remnote2obsidian/cli/`
- `tests/unit/`
- `tests/integration/`

## Scope

- implement the CLI with Typer
- parse input path and output path arguments
- parse dry-run and verbose flags
- call the migration service
- print concise status and diagnostics
- return non-zero exit status on blocking failures

## Out of Scope

- implementing migration workflow logic in the CLI
- adding interactive prompts
- adding watch or sync mode

## Done

- [ ] CLI is implemented with Typer
- [ ] CLI accepts input and output paths
- [ ] CLI supports dry-run mode
- [ ] CLI supports verbose mode
- [ ] CLI delegates to the migration service
- [ ] tests added or updated
- [ ] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: CLI test covers success and failure exit statuses
- Verify: CLI code does not implement domain transformation logic

## Notes

- add Typer as the CLI dependency when implementing this task
- preserve the existing Poetry script name
