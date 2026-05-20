---
feature: FEATURE-004
title: "Generate AI context"
status: planned
created: 2026-05-20
---

# Generate AI context

## Goal

Generate machine-readable context files that help AI agents understand the migrated Obsidian vault structure, source RemNote IDs, generated Markdown paths, and important relationships.

## Problem

Markdown files are optimized for human reading, but AI-assisted workflows also need compact, structured metadata to locate notes, follow relationships, and reason about the migration output. The migration needs a separate AI-context generation step that describes the generated vault without duplicating Markdown rendering logic.

## Scope

- consume the internal graph from FEATURE-002 and generated Markdown path information from FEATURE-003
- generate a manifest mapping original RemNote IDs to generated Markdown paths
- include source metadata needed to trace generated files back to RemNote records
- include relationship summaries such as parent-child links and known references where possible
- include unresolved reference or unsupported-structure summaries where useful for later review
- produce deterministic machine-readable context files for identical migration input
- keep AI-context data focused on navigation, traceability, and agent comprehension

## Out of Scope

- loading or validating RemNote export files
- parsing `rem.json` into the internal graph
- rendering Markdown document bodies
- defining CLI arguments or command behavior
- semantic summarization or automatic note rewriting
- duplicating Markdown generation rules

## Success Criteria

- [ ] generated context includes a manifest mapping RemNote IDs to Markdown paths
- [ ] manifest entries preserve enough metadata to trace each file back to source graph nodes
- [ ] parent-child relationships and known references are represented where available
- [ ] unsupported or unresolved structures can be reported without blocking deterministic output
- [ ] AI-context generation does not duplicate Markdown rendering logic
- [ ] generated context files are deterministic for identical graph and Markdown path input

## Notes

- relates to PRD-001
- depends on FEATURE-002 for graph relationships and FEATURE-003 for generated Markdown paths
- context generation belongs in `domain/` when deriving data and `services/` when coordinating output
- filesystem writing belongs in `adapters/`
- generated files should help future AI agents understand the vault without requiring access to the original export
