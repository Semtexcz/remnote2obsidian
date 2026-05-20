---
task: TASK-025
title: "Add logging and verbose reporting"
status: backlog
priority: P2
type: feature
created: 2026-05-20
related:
  - FEATURE-005
  - US-004
  - US-013
  - US-014
---

# Add logging and verbose reporting

## Goal

Add deterministic progress and diagnostic reporting for normal and verbose CLI runs. Reporting should help users inspect migration behavior without overwhelming standard output.

## Context

Large exports and partially undocumented structures require clear inspection support. The CLI should format diagnostics produced by services and domain modules rather than creating its own migration logic.

## Touchpoints

- `src/remnote2obsidian/cli/`
- `src/remnote2obsidian/services/`
- `tests/unit/`

## Scope

- format errors and warnings consistently
- show concise progress in normal mode
- show additional diagnostics in verbose mode
- keep output ordering deterministic
- add tests for reporting behavior

## Out of Scope

- adding external logging infrastructure
- changing diagnostic model semantics
- writing report files

## Done

- [ ] normal mode reports final status clearly
- [ ] verbose mode includes detailed diagnostics
- [ ] diagnostic order is deterministic
- [ ] blocking errors are easy to identify
- [ ] tests added or updated
- [ ] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: report formatting tests match expected output
- Verify: verbose mode does not change migration results

## Notes

- standard-library logging or explicit formatting is sufficient
- avoid nondeterministic timestamps in testable output
