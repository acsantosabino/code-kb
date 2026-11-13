## Context

See `proposal.md` for motivation. The system requires a systematic approach to analyze all files, entrypoints, and modules in target repositories, group them logically into distinct features, and produce exhaustive PRDs for each feature using the `rag-legado-doc` skill workflow.

## Goals / Non-Goals

**Goals:**
- Provide a systematic multi-step workflow for scanning the codebase.
- Extract high-level features and modules from structural layout and code symbols.
- Sequentially generate complete TDD-oriented PRDs for each inferred feature into `docs/features/`.
- Ensure quality control and validation for every generated PRD document.

**Non-Goals:**
- Modifying the underlying source code of target repository applications.
- Refactoring existing business logic.

## Decisions

### 1. Repository Structure & Feature Discovery Scan
- **Decision**: Perform an automated recursive directory and symbol search using structural rules (e.g. key modules, API routes, domains, CLI apps) to create a list of candidate features.
- **Rationale**: Ensures complete coverage without missing sub-modules or implicit domain capabilities.

### 2. Sequential PRD Generation via RAG Legado Doc Skill
- **Decision**: For each discovered candidate feature, execute the standardized `rag-legado-doc` generator process to query local RAG embeddings and write complete PRDs to `docs/features/<feature>.md`.
- **Rationale**: Leverages established documentation standards, TDD specs, and deep context retrieval to yield high-fidelity PRDs.

## Risks / Trade-offs

- [Risk: Large repository size leading to many features] → Mitigation: Group related sub-modules under cohesive domain feature PRDs.
- [Risk: Incomplete RAG index] → Mitigation: Ensure RAG re-indexing/verification is executed prior to generating docs.
