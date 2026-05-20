# Test Fixtures

These fixtures are small artificial RemNote export samples for deterministic tests.
They do not contain real user data.

- `valid_minimal/`: contains only a valid `rem.json` export envelope.
- `valid_with_optional_files/`: contains `rem.json`, `cards.json`, and `metadata.json`.
- `invalid_json/`: contains an intentionally malformed `rem.json`.
- `missing_rem/`: contains optional metadata without the required `rem.json`.
- `hierarchy_references_attachments/`: contains fake hierarchy, references, unknown fields, and attachment references.
