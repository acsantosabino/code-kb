## Context

See `proposal.md`. The RAG documentation generator (`doc_generator.py`) previously performed broad keyword searches without excluding tool-internal directories (`.agent/`, `rag-legado-skill/`, `docs/features/`). This caused the PRD generator to retrieve chunks from the skill documentation itself.

## Goals / Non-Goals

**Goals:**
- Add negative filtering or path constraints in `doc_generator.py` so retrieval ignores tool/meta paths.
- Guarantee feature segregation based on application module structure.

**Non-Goals:**
- Removing the RAG engine or changing vector store backends.

## Decisions

### 1. Ignore List Filtering in Hybrid Search / Doc Generator
- **Decision**: Filter out any retrieved chunk whose `file_path` contains `.agent/`, `rag-legado-skill/`, `.claude/`, or `docs/features/` unless explicitly targeting those folders.
- **Rationale**: Prevents self-referential skill context leakage into target feature PRDs.

## Risks / Trade-offs

- [Risk: Missing context if app code resides in non-standard paths] → Mitigation: Only exclude known tooling/skill prefix directories.
