---
task: TASK-012
title: "Handle unknown Rem types"
status: done
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-002
  - US-012
---

# Handle unknown Rem types

## Goal

Add explicit handling and diagnostics for RemNote records with unknown or unsupported object types. The migration should preserve these records and continue when they are non-blocking.

## Context

The RemNote export format is partially reverse engineered. The project must preserve unknown fields and object types instead of silently discarding them.

## Touchpoints

- `src/remnote2obsidian/domain/`
- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- identify records with missing or unexpected `type` values
- preserve unknown type values on graph nodes
- produce deterministic warnings for unsupported types when useful
- keep unsupported nodes available for later rendering or manifests

## Out of Scope

- fully interpreting every RemNote type
- blocking migration for all unknown types
- semantic cleanup of unknown content

## Done

- [x] unknown type values remain available
- [x] unsupported types can be reported
- [x] graph construction continues for non-blocking unknown types
- [x] unknown records can be inspected after parsing
- [x] tests added or updated
- [x] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: fixture with unknown type preserves the record
- Verify: warnings are stable and source-linked

## Notes

- preservation is more important than aggressive interpretation
- this task should not add Markdown rendering behavior
