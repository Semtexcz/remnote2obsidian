---
task: TASK-017
title: "Generate stable Markdown paths"
status: backlog
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-003
  - US-008
  - US-010
---

# Generate stable Markdown paths

## Goal

Generate deterministic Markdown file paths for graph nodes. Paths should be safe for filesystem output, stable across repeated runs, and suitable for Obsidian navigation.

## Context

Obsidian-compatible output needs predictable file paths. Repeated migrations must not produce path churn for identical input.

## Touchpoints

- `src/remnote2obsidian/domain/`
- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- generate Markdown paths from graph node content and IDs
- handle duplicate or empty titles deterministically
- keep paths safe for common filesystems
- preserve a path mapping from RemNote IDs to Markdown paths
- add tests for duplicate titles and stable path generation

## Out of Scope

- writing files to disk
- creating AI manifests
- syncing with an existing vault

## Done

- [ ] every renderable graph node gets a stable path
- [ ] duplicate titles do not collide
- [ ] paths include enough stability to survive repeated runs
- [ ] path mapping preserves RemNote IDs
- [ ] tests added or updated
- [ ] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: duplicate-title fixture produces unique paths
- Verify: repeated path generation is identical

## Notes

- favor deterministic ID-backed paths over fragile title-only paths
- keep path generation independent of filesystem writes
