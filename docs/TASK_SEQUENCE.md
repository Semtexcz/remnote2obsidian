# Task Sequence

## Order

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

### AI Context

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

TASK-001 through TASK-019 are complete. The remaining MVP path is TASK-020 through TASK-026. TASK-027 and TASK-028 harden the project for real-export validation and user-facing usage after the core workflow is working.
