---
story: US-011
title: "Preserve attachment references"
status: draft
created: 2026-05-20
related:
  - FEATURE-002
  - FEATURE-003
  - FEATURE-004
---

# Preserve attachment references

## As a

RemNote user with files and images in notes

## I want

attachment references from my RemNote export to be preserved

## So that

I do not lose track of linked images, PDFs, or other files during migration.

## Scope

- preserve attachment references found in RemNote data
- keep local placeholder references inspectable
- keep remote asset URLs inspectable
- include attachment relationship information where useful for Markdown and AI context

## Out of Scope

- downloading remote assets
- repairing broken attachment URLs
- guaranteeing that external asset hosts remain available

## Acceptance

- [ ] attachment references are not silently discarded
- [ ] local placeholder references remain visible or traceable
- [ ] remote asset URLs remain visible or traceable
- [ ] generated Markdown preserves attachment context where possible
- [ ] AI-readable context can help locate notes with attachment references

## Notes

- supports PRD-001 attachment preservation
- RemNote exports may contain `%LOCAL_FILE%...` placeholders and remote URLs
