---
task: TASK-026
title: "Add end-to-end MVP test"
status: backlog
priority: P1
type: test
created: 2026-05-20
related:
  - FEATURE-001
  - FEATURE-002
  - FEATURE-003
  - FEATURE-004
  - FEATURE-005
  - US-001
  - US-010
---

# Add end-to-end MVP test

## Goal

Add an end-to-end test that runs the CLI or migration service on a small fixture and verifies the generated vault and AI context output.

## Context

The MVP needs confidence that the main workflow works from input export to generated output. The test should remain deterministic and fast.

## Touchpoints

- `tests/integration/`
- `tests/fixtures/`
- `src/remnote2obsidian/`

## Scope

- run a full migration against a small fixture
- verify generated Markdown files exist
- verify original RemNote IDs are present in output
- verify AI manifest exists and maps IDs to paths
- verify repeated runs produce identical output

## Out of Scope

- testing the full real export
- comparing every Markdown formatting detail
- testing Obsidian itself

## Done

- [ ] e2e or integration MVP test exists
- [ ] generated vault output is verified
- [ ] AI manifest output is verified
- [ ] deterministic rerun behavior is verified
- [ ] tests added or updated
- [ ] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: test uses temporary output directories
- Verify: test is deterministic and fast

## Notes

- use the smallest fixture that exercises the full pipeline
- this task should catch integration gaps across layers
