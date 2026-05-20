---
task: TASK-003
title: "Define migration result models"
status: done
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-001
  - FEATURE-002
  - FEATURE-005
  - US-004
---

# Define migration result models

## Goal

Define shared result and diagnostic models for validation errors, warnings, and migration summaries. These models should support clear reporting without mixing domain logic into the CLI.

## Context

Multiple features need consistent reporting for missing files, invalid JSON, graph issues, unknown structures, and dry-run summaries. A small shared model layer will keep reporting deterministic and testable.

## Touchpoints

- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- define a validation severity model for errors and warnings
- define a diagnostic message model with code, message, and optional source context
- define a generic result container for data plus diagnostics
- add tests for deterministic ordering and basic construction

## Out of Scope

- implementing file loading
- implementing graph validation
- formatting CLI output

## Done

- [x] diagnostic models exist
- [x] errors and warnings can be represented separately
- [x] source context can identify files or RemNote IDs
- [x] models are deterministic and type hinted
- [x] tests added or updated
- [x] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: model tests cover errors, warnings, and success cases
- Verify: models do not depend on CLI or filesystem modules

## Notes

- keep models small and explicit
- prefer dataclasses or similarly simple standard-library structures
