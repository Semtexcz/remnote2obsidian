---
story: US-008
title: "Open generated vault in Obsidian"
status: draft
created: 2026-05-20
related:
  - FEATURE-003
---

# Open generated vault in Obsidian

## As a

Obsidian user

## I want

the migration output to behave like an Obsidian-compatible vault

## So that

I can navigate migrated notes using Obsidian conventions.

## Scope

- generate a directory of Markdown files suitable for opening in Obsidian
- use Obsidian-compatible links where possible
- keep note paths stable and deterministic
- preserve unresolved references in an inspectable form

## Out of Scope

- installing or configuring Obsidian plugins
- generating a custom Obsidian theme
- implementing live synchronization with Obsidian

## Acceptance

- [ ] output directory can be opened as an Obsidian vault
- [ ] generated Markdown files are discoverable in Obsidian
- [ ] known internal references become navigable links where possible
- [ ] unresolved links do not cause data loss
- [ ] vault structure remains stable across repeated migrations

## Notes

- supports PRD-001 Obsidian output goal
- compatibility should not require proprietary RemNote behavior
