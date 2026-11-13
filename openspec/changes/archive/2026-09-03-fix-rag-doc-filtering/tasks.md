## 1. Filter Implementation in `doc_generator.py`

- [x] 1.1 Update `generate_module_doc` in `rag-legado-skill/mcp_server/doc_generator.py` to filter out chunks from `.agent/`, `rag-legado-skill/`, `.claude/`, and `docs/features/`.
- [x] 1.2 Add target feature path matching logic to ensure retrieval focuses on target application source files.

## 2. Validation & Regeneration

- [x] 2.1 Re-run PRD generation for application features and verify that output documents describe application capabilities rather than skill tooling.
