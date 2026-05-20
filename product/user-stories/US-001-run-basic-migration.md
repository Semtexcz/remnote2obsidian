---
story: US-001
title: "Run a basic migration"
status: draft
created: 2026-05-20
related:
  - FEATURE-001
  - FEATURE-002
  - FEATURE-003
  - FEATURE-004
  - FEATURE-005
---

# Run a basic migration

## As a

RemNote user migrating to Obsidian

## I want

to run one migration command against my RemNote export

## So that

I can create an Obsidian vault from my existing knowledge base without manually converting files.

## Scope

- migrate from a RemNote export directory to an Obsidian vault directory
- produce Markdown files and AI-readable context files
- keep the source export unchanged
- report whether the migration completed successfully

## Out of Scope

- bidirectional synchronization
- interactive editing during migration
- perfect recreation of RemNote behavior

## Acceptance

- [ ] a user can provide an export path and output path
- [ ] migration completes when the export is valid
- [ ] generated output can be opened as an Obsidian vault
- [ ] source export files remain unchanged
- [ ] migration result includes a clear success or failure status

## Notes

- relates to PRD-001 end-to-end workflow
- output should prioritize preservation over aggressive transformation
