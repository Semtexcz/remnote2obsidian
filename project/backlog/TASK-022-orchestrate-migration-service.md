---
task: TASK-022
title: "Orchestrate migration service"
status: backlog
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-001
  - FEATURE-002
  - FEATURE-003
  - FEATURE-004
  - US-001
  - US-010
---

# Orchestrate migration service

## Goal

Create a service that coordinates the full migration workflow from export loading through graph parsing, Markdown generation, AI manifest generation, and output writing.

## Context

Services may coordinate adapters and domain modules. The CLI should remain thin and delegate the workflow to this service.

## Touchpoints

- `src/remnote2obsidian/services/`
- `src/remnote2obsidian/adapters/`
- `src/remnote2obsidian/domain/`
- `tests/integration/`

## Scope

- define migration service inputs and summary output
- call export loading and validation steps
- call graph construction and rendering steps
- call Markdown and AI context writers
- aggregate diagnostics and final status

## Out of Scope

- parsing CLI arguments
- adding new rendering behavior
- using the full real export as a required test fixture

## Done

- [ ] service coordinates the migration pipeline
- [ ] service returns success, warnings, and errors
- [ ] service preserves read-only source behavior
- [ ] integration test covers a small valid fixture
- [ ] tests added or updated
- [ ] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: fixture migration writes Markdown and AI context output
- Verify: source fixture files remain unchanged

## Notes

- keep orchestration explicit and boring
- do not let services absorb domain transformation logic
