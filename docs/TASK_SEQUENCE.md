# Task Sequence

## Order

- TASK-022 Orchestrate migration service
- TASK-023 Add dry-run service mode
- TASK-024 Add CLI entrypoint
- TASK-025 Add logging and verbose reporting
- TASK-026 Add end-to-end MVP test
- TASK-027 Add large export smoke test
- TASK-028 Document MVP usage

## Dependencies

### MVP Orchestration

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

TASK-001 through TASK-021 are complete. The remaining MVP path is TASK-022 through TASK-026. TASK-027 and TASK-028 harden the project for real-export validation and user-facing usage after the core workflow is working.
