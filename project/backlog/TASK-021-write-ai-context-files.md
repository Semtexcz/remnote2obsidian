---
task: TASK-021
title: "Write AI context files"
status: backlog
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-004
  - US-009
---

# Write AI context files

## Goal

Write generated AI context files into the output vault. The files should be deterministic, machine-readable, and easy for future agents to locate.

## Context

Manifest derivation belongs in domain logic, while filesystem writing belongs in adapters. This task adds the adapter-level write behavior for AI context outputs.

## Touchpoints

- `src/remnote2obsidian/adapters/`
- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- write manifest JSON to a stable path in the output vault
- create AI context directory structure if needed
- report write diagnostics
- keep output deterministic for identical manifest input
- add tests using temporary directories

## Out of Scope

- deriving manifest content
- rendering Markdown files
- defining CLI options

## Done

- [ ] AI manifest is written to a stable output path
- [ ] output directory is created as needed
- [ ] file content is deterministic
- [ ] write failures are reported
- [ ] tests added or updated
- [ ] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: temporary output contains the expected context file
- Verify: repeated writes produce identical content

## Notes

- choose a simple path such as an internal metadata directory
- avoid exposing sensitive metadata beyond what manifest generation provides
