---
task: TASK-023
title: "Add dry-run service mode"
status: backlog
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-005
  - US-013
  - US-004
---

# Add dry-run service mode

## Goal

Add dry-run support to the migration service so users can validate and inspect a migration without writing output files.

## Context

Dry-run mode is part of the CLI feature, but the behavior should live in services so the CLI remains thin. Dry run should still exercise loading, validation, and planning.

## Touchpoints

- `src/remnote2obsidian/services/`
- `tests/integration/`

## Scope

- add a dry-run option to service inputs
- run loading and validation in dry-run mode
- run graph construction enough to report planning diagnostics
- skip Markdown and AI context file writes
- report what would be generated

## Out of Scope

- parsing CLI flags
- writing preview files
- changing source export files

## Done

- [ ] dry-run mode produces no output files
- [ ] dry-run mode reports validation status
- [ ] dry-run mode reports planned output counts where available
- [ ] blocking errors are visible
- [ ] tests added or updated
- [ ] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: dry-run integration test leaves output directory empty or absent
- Verify: dry-run diagnostics are deterministic

## Notes

- dry run must not call output adapters for file writes
- keep behavior useful for large export inspection
