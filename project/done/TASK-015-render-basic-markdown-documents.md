---
task: TASK-015
title: "Render basic Markdown documents"
status: done
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-003
  - US-007
---

# Render basic Markdown documents

## Goal

Render graph nodes into basic Markdown document content. The renderer should convert preserved text content into readable Markdown without writing files or defining vault paths.

## Context

Markdown rendering belongs in domain transformation logic and must remain separate from filesystem writing and CLI orchestration.

## Touchpoints

- `src/remnote2obsidian/domain/`
- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- define a Markdown document model with path placeholder and content
- render graph node title/content into Markdown text
- render child content in a deterministic order
- include fallback text for unsupported fragments
- add renderer unit tests

## Out of Scope

- writing Markdown files to disk
- generating YAML frontmatter
- generating Obsidian wikilinks
- AI manifest generation

## Done

- [x] graph nodes can render to Markdown document content
- [x] rendering is deterministic
- [x] unsupported fragments remain visible or represented
- [x] renderer has no filesystem dependency
- [x] tests added or updated
- [x] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: simple graph fixture renders expected Markdown
- Verify: repeated rendering returns identical content

## Notes

- keep formatting simple for MVP
- preserve rather than optimize content
