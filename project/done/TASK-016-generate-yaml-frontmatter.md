---
task: TASK-016
title: "Generate YAML frontmatter"
status: done
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-003
  - US-006
  - US-007
---

# Generate YAML frontmatter

## Goal

Add deterministic YAML frontmatter to generated Markdown documents. Frontmatter must preserve original RemNote IDs and key traceability metadata.

## Context

Original RemNote IDs must always be preserved. Frontmatter provides a stable, human-readable way to keep source metadata available in Obsidian and Git.

## Touchpoints

- `src/remnote2obsidian/domain/`
- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- include original RemNote `_id` in frontmatter
- include parent ID and type when available
- include card metadata summary when available
- serialize frontmatter deterministically
- add tests for stable frontmatter output

## Out of Scope

- exposing sensitive user metadata by default
- generating AI manifest files
- writing files to disk

## Done

- [x] frontmatter includes original RemNote ID
- [x] metadata keys are ordered deterministically
- [x] optional metadata is included only when available
- [x] output remains valid Markdown
- [x] tests added or updated
- [x] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: frontmatter fixture matches expected output
- Verify: repeated rendering produces identical frontmatter

## Notes

- avoid adding a YAML dependency unless clearly justified
- keep serialized metadata minimal and traceable
