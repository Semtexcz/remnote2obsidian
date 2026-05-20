# Task Sequence

## Order

- TASK-004 Implement JSON file adapter
- TASK-005 Load RemNote export directory
- TASK-006 Validate export envelope
- TASK-007 Define raw RemNote models
- TASK-008 Parse raw Rem documents
- TASK-009 Parse rich text fragments
- TASK-010 Build Rem graph nodes
- TASK-011 Reconstruct Rem hierarchy
- TASK-012 Handle unknown Rem types
- TASK-013 Integrate card metadata
- TASK-014 Extract attachment references
- TASK-015 Render basic Markdown documents
- TASK-016 Generate YAML frontmatter
- TASK-017 Generate stable Markdown paths
- TASK-018 Render Obsidian wikilinks
- TASK-019 Write Obsidian vault files
- TASK-020 Generate AI manifest
- TASK-021 Write AI context files
- TASK-022 Orchestrate migration service
- TASK-023 Add dry-run service mode
- TASK-024 Add CLI entrypoint
- TASK-025 Add logging and verbose reporting
- TASK-026 Add end-to-end MVP test
- TASK-027 Add large export smoke test
- TASK-028 Document MVP usage

## Dependencies

### Loading and Validation

- TASK-005 <- TASK-004
- TASK-006 <- TASK-005

### Parsing and Graph

- TASK-007 <- TASK-006
- TASK-008 <- TASK-007
- TASK-009 <- TASK-008
- TASK-010 <- TASK-008, TASK-009
- TASK-011 <- TASK-010
- TASK-012 <- TASK-010
- TASK-013 <- TASK-010
- TASK-014 <- TASK-010

### Markdown and Obsidian Output

- TASK-015 <- TASK-011, TASK-012
- TASK-016 <- TASK-015
- TASK-017 <- TASK-015
- TASK-018 <- TASK-017
- TASK-019 <- TASK-016, TASK-017, TASK-018

### AI Context

- TASK-020 <- TASK-011, TASK-014, TASK-017
- TASK-021 <- TASK-020

### MVP Orchestration

- TASK-022 <- TASK-019, TASK-021
- TASK-023 <- TASK-022
- TASK-024 <- TASK-023
- TASK-025 <- TASK-024
- TASK-026 <- TASK-024
- TASK-027 <- TASK-026
- TASK-028 <- TASK-026

## Rule

Follow the first unfinished task in Order.  
Do not violate Dependencies.

## MVP Path

TASK-001 through TASK-003 are complete. The remaining MVP path is TASK-004 through TASK-026. TASK-027 and TASK-028 harden the project for real-export validation and user-facing usage after the core workflow is working.
