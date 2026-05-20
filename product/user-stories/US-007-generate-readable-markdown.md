---
story: US-007
title: "Generate readable Markdown"
status: draft
created: 2026-05-20
related:
  - FEATURE-003
---

# Generate readable Markdown

## As a

Obsidian user

## I want

my RemNote content converted into readable Markdown files

## So that

I can browse and edit my migrated knowledge base in a portable format.

## Scope

- generate Markdown files from migrated RemNote graph data
- render available note content in a readable form
- keep generated files Git-friendly
- preserve unsupported or unresolved content in an inspectable way

## Out of Scope

- perfect visual recreation of RemNote
- AI-context manifest generation
- command-line interface design

## Acceptance

- [ ] generated files use Markdown format
- [ ] generated content is readable in a text editor
- [ ] generated files remain stable for identical input
- [ ] unsupported content is preserved or reported
- [ ] generated output avoids unnecessary noise that would make diffs hard to review

## Notes

- supports PRD-001 portable Markdown output
- Markdown output should favor clarity and preservation
