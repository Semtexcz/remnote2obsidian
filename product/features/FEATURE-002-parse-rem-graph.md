---
feature: FEATURE-002
title: "Parse Rem graph"
status: planned
created: 2026-05-20
---

# Parse Rem graph

## Goal

Parse loaded RemNote export data into an internal graph representation that preserves RemNote identity, hierarchy, content fields, references, and available card metadata for later migration steps.

## Problem

RemNote stores knowledge as interconnected JSON documents rather than as standalone Markdown files. The migration needs a deterministic graph-building step that turns validated `rem.json` data into domain structures without losing unknown fields or coupling parsing to Markdown generation.

## Scope

- consume loaded export data produced by FEATURE-001
- parse `rem.json` records into internal graph nodes keyed by original `_id`
- preserve `_id`, `parent`, `children`, `subBlocks`, `key`, `value`, `type`, and references where available
- preserve unknown fields and nested structures for future migration improvements
- build parent-child relationships from explicit hierarchy fields where available
- attach card metadata from `cards.json` by matching `cards.json` `rId` to rem `_id` when available
- report graph validation issues such as missing IDs, duplicate IDs, broken parent links, or card references without matching rems

## Out of Scope

- loading files from disk
- generating Markdown or Obsidian links
- writing output files
- generating AI-readable context files or manifests
- fully interpreting all RemNote object types
- implementing spaced repetition behavior

## Success Criteria

- [ ] loaded `rem.json` records are represented as internal graph nodes keyed by original `_id`
- [ ] hierarchy fields are preserved and converted into deterministic graph relationships
- [ ] `key`, `value`, `type`, and reference-related fields remain available on graph nodes
- [ ] card metadata from `cards.json` is attached when matching `rId` values exist
- [ ] unknown fields and structures are preserved without silent discard
- [ ] graph validation issues are reported clearly without writing output files
- [ ] parsing behavior is deterministic for identical loaded export data

## Notes

- relates to PRD-001
- depends on FEATURE-001 for loaded and validated export data
- core graph logic belongs in `domain/`
- validation must remain separate from Markdown transformation logic
- `context/remnote/JSON_DOKUMENTACE.md` documents the current reverse-engineered interpretation of `rem.json` and `cards.json`
