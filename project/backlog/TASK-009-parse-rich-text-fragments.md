---
task: TASK-009
title: "Parse rich text fragments"
status: backlog
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-002
  - FEATURE-003
  - US-007
  - US-012
---

# Parse rich text fragments

## Goal

Represent RemNote `key` and `value` fragments in a preservation-first internal format. The parser should support simple strings and structured reference fragments without losing unsupported fragment data.

## Context

`key` and `value` can contain plain strings or structured objects such as references. Markdown generation needs a stable representation, but unsupported structures must remain inspectable.

## Touchpoints

- `src/remnote2obsidian/domain/`
- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- parse plain string fragments
- parse structured reference fragments that contain target IDs
- preserve unsupported fragment objects as raw data
- report unsupported fragment shapes as warnings when useful
- add unit tests for plain text, references, and unknown fragments

## Out of Scope

- rendering Markdown
- resolving links to output paths
- fully implementing RemNote rich text semantics

## Done

- [ ] plain text fragments are represented
- [ ] reference fragments preserve target RemNote IDs
- [ ] unsupported fragments are preserved
- [ ] warnings are deterministic
- [ ] tests added or updated
- [ ] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: unknown fragment data is not discarded
- Verify: parser has no filesystem dependency

## Notes

- preserve first, interpret only known safe structures
- keep rendering decisions for later Markdown tasks
