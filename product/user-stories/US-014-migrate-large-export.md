---
story: US-014
title: "Migrate large export"
status: draft
created: 2026-05-20
related:
  - FEATURE-001
  - FEATURE-002
  - FEATURE-003
  - FEATURE-004
  - FEATURE-005
---

# Migrate large export

## As a

RemNote user with a large knowledge base

## I want

the migration tool to handle a large real-world export predictably

## So that

I can migrate my full knowledge base instead of only small test examples.

## Scope

- support migration of large RemNote exports
- keep validation and progress reporting understandable
- preserve hierarchy, IDs, metadata, references, and attachments where possible
- produce deterministic output suitable for review

## Out of Scope

- requiring the user to split the export manually
- optimizing every note semantically
- hiding warnings because the export is large

## Acceptance

- [ ] large exports can be loaded and validated
- [ ] large graph data can be migrated without changing source files
- [ ] warnings remain inspectable for large migrations
- [ ] generated Markdown and AI context remain deterministic
- [ ] output remains organized enough for Obsidian and Git review

## Notes

- supports PRD-001 real export success criteria
- large exports should use representative fixtures or controlled test data during implementation planning
