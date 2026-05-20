---
task: TASK-014
title: "Extract attachment references"
status: done
priority: P2
type: feature
created: 2026-05-20
related:
  - FEATURE-002
  - FEATURE-003
  - FEATURE-004
  - US-011
---

# Extract attachment references

## Goal

Detect and preserve attachment references embedded in RemNote data. The graph should expose local placeholders and remote asset URLs so Markdown and AI-context output can reference them later.

## Context

RemNote exports may contain `%LOCAL_FILE%...` placeholders and S3 URLs inside rich content or nested structures. The first version should preserve references, not download or repair them.

## Touchpoints

- `src/remnote2obsidian/domain/`
- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- detect `%LOCAL_FILE%...` references in parsed content or raw structures
- detect HTTP asset URLs in parsed content or raw structures
- attach discovered references to graph nodes
- preserve source context for each discovered attachment reference
- add tests for local placeholders and remote URLs

## Out of Scope

- downloading attachments
- copying attachment files
- validating remote URL availability

## Done

- [x] local attachment placeholders are detected
- [x] remote asset URLs are detected
- [x] attachment references remain linked to source Rem IDs
- [x] unknown surrounding structures are preserved
- [x] tests added or updated
- [x] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: attachment fixture exposes references on graph nodes
- Verify: no network access is required

## Notes

- extraction should be deterministic and read-only
- avoid broad transformations of raw nested data
