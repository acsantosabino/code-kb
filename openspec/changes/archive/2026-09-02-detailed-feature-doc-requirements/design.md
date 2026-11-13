## Context

See proposal.md for overall motivation. The project uses RAG and specialized agent skills (`rag-legado-skill` and `rag-legado-doc`) to generate technical documentation for legacy and new modules under `docs/features/`.

## Goals / Non-Goals

**Goals:**
- Update the documentation generation prompt structure and template in `rag-legado-doc` to explicitly generate a complete, standalone PRD (Product Requirement Document) for each feature.
- Enforce standard PRD sections across generated docs under `docs/features/<feature>.md`: Executive Summary & Objectives, User Stories/Use Cases, Functional Requirements, Non-Functional Requirements & Constraints, Data Models & System Architecture, Dependencies & Integrations, Edge Cases & Error Handling, TDD Test Suites (Unit, Integration, E2E), and Reproduction Blueprint.

**Non-Goals:**
- Modifying vector DB indexing/retrieval algorithms.
- Re-indexing unrelated repository components.

## Decisions

### Decision 1: Explicit PRD Document Standard per Feature
- **Rationale**: Generating a formal PRD for each feature ensures that every module has exhaustive functional, architectural, and TDD specifications, making features 100% reproducible in new projects.
- **Alternatives Considered**: Lightweight Markdown summaries (discarded due to lack of reproduction completeness).

### Decision 2: Segmented Generation per Context Chunks
- **Rationale**: Large feature modules produce extensive context chunk sets from RAG retrieval. Segmenting PRD generation per context chunks (or PRD sections) prevents context window overflow, avoids truncation, and ensures deep technical detail capture across all chunks.
- **Alternatives Considered**: Single-pass generation with concatenated chunks (discarded due to risk of context window truncation and loss of detail).

## Risks / Trade-offs

- [Risk] Multi-chunk segmentation may produce duplicate requirement statements across sections → Mitigation: Include a consolidation/deduplication pass when assembling final PRD sections.
