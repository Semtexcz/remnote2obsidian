---
task: TASK-020
title: "Generate AI manifest"
status: done
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-004
  - US-009
  - US-006
---

# Generate AI manifest

## Goal

Generate a deterministic machine-readable manifest mapping original RemNote IDs to generated Markdown paths. The manifest should help AI agents and users trace migrated content.

## Context

AI-agent compatibility is a core requirement. The manifest must complement Markdown output without duplicating Markdown rendering logic.

## Touchpoints

- `src/remnote2obsidian/domain/`
- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- define an AI manifest model
- include RemNote ID to Markdown path mappings
- include parent IDs and known reference IDs where available
- include attachment reference summaries where available
- serialize manifest deterministically

## Out of Scope

- semantic note summarization
- duplicating Markdown document bodies
- writing manifest files to disk

## Done

- [x] manifest maps RemNote IDs to Markdown paths
- [x] manifest includes useful relationship metadata
- [x] manifest serialization is deterministic
- [x] original RemNote IDs are preserved
- [x] tests added or updated
- [x] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: manifest fixture matches expected JSON
- Verify: repeated manifest generation is identical

## Notes

- prefer JSON for MVP machine-readable output
- order manifest entries deterministically
