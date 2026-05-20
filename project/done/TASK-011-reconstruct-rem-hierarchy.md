---
task: TASK-011
title: "Reconstruct Rem hierarchy"
status: done
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-002
  - US-005
---

# Reconstruct Rem hierarchy

## Goal

Add deterministic parent-child relationships to the internal graph. The hierarchy should use `parent`, `children`, and `subBlocks` where available and report broken or inconsistent links.

## Context

Hierarchy preservation is a core PRD requirement. RemNote exports may contain multiple hierarchy fields, so graph construction must preserve available relationships without guessing aggressively.

## Touchpoints

- `src/remnote2obsidian/domain/`
- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- connect graph nodes using `parent` fields
- preserve explicit `children` and `subBlocks` order where available
- report references to missing parent or child IDs
- expose root nodes deterministically
- add hierarchy-focused tests

## Out of Scope

- choosing Markdown folder structure
- rendering nested Markdown
- repairing broken source hierarchy

## Done

- [x] parent-child relationships are available on graph output
- [x] root nodes are deterministic
- [x] broken links produce diagnostics
- [x] child ordering is stable
- [x] tests added or updated
- [x] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: hierarchy fixture reconstructs expected relationships
- Verify: broken hierarchy fixture reports warnings or errors clearly

## Notes

- preserve source relationships even when incomplete
- avoid silently dropping orphaned nodes
