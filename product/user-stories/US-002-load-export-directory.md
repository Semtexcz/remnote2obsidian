---
story: US-002
title: "Load export directory"
status: draft
created: 2026-05-20
related:
  - FEATURE-001
---

# Load export directory

## As a

RemNote user

## I want

the migration tool to load my RemNote export directory

## So that

the migration can start from the files produced by RemNote without requiring manual preparation.

## Scope

- accept a directory containing RemNote JSON export files
- require `rem.json` as the primary export file
- recognize optional export files when present
- treat all export files as read-only input

## Out of Scope

- parsing RemNote graph relationships
- generating Markdown output
- modifying export files

## Acceptance

- [ ] a valid export directory containing `rem.json` is accepted
- [ ] optional export files are recognized when present
- [ ] missing optional files do not block loading
- [ ] source files are not modified
- [ ] loading results are available for later migration steps

## Notes

- supports PRD-001 loading scope
- related optional files include `cards.json` and `metadata.json`
