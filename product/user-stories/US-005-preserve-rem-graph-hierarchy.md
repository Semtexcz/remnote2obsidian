---
story: US-005
title: "Preserve Rem hierarchy"
status: draft
created: 2026-05-20
related:
  - FEATURE-002
  - FEATURE-003
---

# Preserve Rem hierarchy

## As a

RemNote user

## I want

the hierarchy from my RemNote knowledge base to be preserved

## So that

my migrated vault keeps the structure and context of my original notes.

## Scope

- preserve parent-child relationships from RemNote data
- preserve available child ordering where possible
- carry hierarchy into generated Markdown or vault structure
- make hierarchy recoverable after migration

## Out of Scope

- redesigning the user's knowledge structure
- merging unrelated branches
- automatic semantic reorganization

## Acceptance

- [ ] Rems with parents remain connected to their parent context
- [ ] child relationships remain visible or recoverable in output
- [ ] generated Markdown reflects hierarchy consistently
- [ ] hierarchy preservation is deterministic across repeated runs
- [ ] missing or broken hierarchy links are reported when detected

## Notes

- supports PRD-001 hierarchy preservation
- related to graph parsing and Markdown generation
