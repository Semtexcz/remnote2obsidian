---
task: TASK-007
title: "Define raw RemNote models"
status: done
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-002
  - US-006
  - US-012
---

# Define raw RemNote models

## Goal

Define raw models for RemNote export documents that preserve known fields and unknown data. These models should provide a typed boundary between loaded JSON and graph construction.

## Context

The RemNote format is partially undocumented. Known fields must be easy to access, while unknown fields and structures must not be silently discarded.

## Touchpoints

- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- define a raw Rem document model
- preserve `_id`, `parent`, `children`, `subBlocks`, `key`, `value`, `type`, and reference fields
- preserve unknown fields in an explicit structure
- define a raw card metadata model for `cards.json`
- add tests for known and unknown field preservation

## Out of Scope

- building graph relationships
- rendering Markdown
- interpreting all RemNote object types

## Done

- [x] raw Rem model preserves known fields
- [x] raw Rem model preserves unknown fields
- [x] raw card model preserves `rId` and scheduling metadata
- [x] models tolerate optional and missing fields
- [x] tests added or updated
- [x] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: fixture records with unknown fields round-trip through raw models
- Verify: original RemNote IDs remain available

## Notes

- model creation should be deterministic
- avoid aggressive validation in raw models
