---
feature: FEATURE-003
title: "Generate Markdown"
status: planned
created: 2026-05-20
---

# Generate Markdown

## Goal

Convert the internal Rem graph into deterministic Markdown documents that can be opened and navigated in Obsidian while preserving source identity and hierarchy.

## Problem

Raw RemNote graph data is not directly usable as an Obsidian vault. The migration needs a focused Markdown generation step that renders graph nodes into stable Markdown files, preserves original RemNote IDs, and creates Obsidian-compatible links where possible without mixing in CLI behavior or AI-context generation.

## Scope

- consume the internal graph produced by FEATURE-002
- generate Markdown document content from graph nodes
- preserve RemNote hierarchy in document structure, folder structure, headings, or stable metadata as appropriate
- preserve original RemNote `_id` values in frontmatter or other stable metadata
- render `key` and `value` content into readable Markdown where possible
- generate Obsidian-compatible links for known RemNote references where target Markdown paths are available
- preserve unresolved references and unknown structures in stable metadata or explicit fallback output
- produce deterministic Markdown paths and content for identical graph input

## Out of Scope

- loading or validating RemNote export files
- parsing `rem.json` into the internal graph
- generating AI context manifests or machine-readable agent files
- defining CLI arguments or command behavior
- implementing a full RemNote renderer
- modifying the source export files

## Success Criteria

- [ ] internal graph input produces Markdown documents deterministically
- [ ] generated Markdown preserves original RemNote IDs in frontmatter or stable metadata
- [ ] hierarchy from the graph remains visible or recoverable in the generated vault
- [ ] known references are rendered as Obsidian-compatible links where possible
- [ ] unresolved or unknown structures are not silently discarded
- [ ] Markdown generation does not contain CLI or file-loading logic
- [ ] generated output remains Git-friendly and human-readable

## Notes

- relates to PRD-001
- depends on FEATURE-002 for the internal graph
- Markdown transformation logic belongs in `domain/`
- filesystem writing belongs in `adapters/` and workflow coordination belongs in `services/`
- this feature must not duplicate or define AI-context manifest generation
