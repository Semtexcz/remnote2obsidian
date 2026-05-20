---
task: TASK-018
title: "Render Obsidian wikilinks"
status: backlog
priority: P1
type: feature
created: 2026-05-20
related:
  - FEATURE-003
  - US-008
---

# Render Obsidian wikilinks

## Goal

Render known internal RemNote references as Obsidian-compatible wikilinks when target Markdown paths are available. Unresolved references must remain inspectable and must not cause data loss.

## Context

RemNote content may contain references to other Rems. Obsidian output should make known references navigable while preserving unresolved or unsupported references.

## Touchpoints

- `src/remnote2obsidian/domain/`
- `src/remnote2obsidian/models/`
- `tests/unit/`

## Scope

- resolve parsed reference fragments through the RemNote ID to Markdown path mapping
- render known references as wikilinks
- render unresolved references with source ID fallback text
- keep link output deterministic
- add tests for resolved and unresolved references

## Out of Scope

- backlink indexing
- Obsidian plugin configuration
- resolving external URLs beyond preserving them

## Done

- [ ] known RemNote references become wikilinks
- [ ] unresolved references preserve target IDs
- [ ] link rendering is deterministic
- [ ] Markdown remains readable
- [ ] tests added or updated
- [ ] docs updated if behavior changed

## Validation

- Run: `poetry run pytest`
- Verify: reference fixture renders expected wikilinks
- Verify: missing target fixture preserves unresolved ID

## Notes

- do not silently drop broken references
- this task depends on stable path mapping
