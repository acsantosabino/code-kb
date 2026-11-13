## Why

When generating feature documentation for target repositories using `doc_generator.py` / `rag-legado-doc`, the RAG query retrieval currently matches internal skill tooling files (`.agent/skills/`, `rag-legado-skill/`, `docs/features/`) because query filters and path scopes are not strict. As a result, generated PRD docs describe the RAG skill itself rather than target project features. Additionally, feature segregation by business domain is lacking.

## What Changes

- **Strict File-Path Filtering in `doc_generator.py`**: Exclude skill meta-files (`.agent/`, `rag-legado-skill/`, `.claude/`, `docs/`) from context retrieval when documenting application target features.
- **Domain Feature Segregation**: Improve `caminho_ou_nome` query expansion and path matching to isolate domain modules and prevent skill context leakage into feature PRDs.

## Capabilities

### New Capabilities
- `feature-doc-isolation`: Strict path filtering and domain feature segregation in PRD doc generation to prevent skill self-documentation.

### Modified Capabilities

## Impact

- `rag-legado-skill/mcp_server/doc_generator.py`: Update query filters and retrieval logic.
- `docs/features/`: Clean PRD documents generated exclusively from application code.
