## Context

This change consolidates six existing OpenSpec specifications (`rag-engine`, `hybrid-search`, `mcp-server`, `agent-skills`, `feature-doc-isolation`, `per-feature-prd-catalog`) into a unified `system-capabilities` specification. These specs were developed incrementally across archived changes (`local-rag-code-kb`, `detailed-feature-doc-requirements`, `fix-rag-doc-filtering`, `per-feature-prd-docs`) and now form the complete operational contract of the RAG/Legacy Documentation ecosystem. The consolidation creates a single source of truth for the system's current behavioral contract without modifying any underlying implementation.

Current system state:
- Six separate specs defining related but independent capability areas
- Clear architectural boundaries and well-scoped requirements in each spec
- No current implementation changes needed; the system already operates according to all existing specs
- Need for a centralized, unified reference for architectural clarity and system completeness

## Goals / Non-Goals

**Goals:**
- Create a unified specification document (`system-capabilities`) that consolidates all current RAG/Legacy Documentation ecosystem capabilities in one place
- Provide a single authoritative reference for the complete operational contract of the system
- Maintain all existing behavioral requirements and architectural constraints from the six source specs
- Establish a clear architectural foundation for future enhancements and changes
- Ensure all current capabilities are testable and explicitly documented with scenarios

**Non-Goals:**
- Modify any existing implementation code in the `rag-legado-skill` module
- Change external behavior or contracts of any existing capability
- Add new capabilities beyond consolidation
- Modify post-commit hooks, MCP server interfaces, or retrieval pipelines
- Create separate consolidated documentation in addition to this spec (spec is the single source of truth)

## Decisions

1. **Consolidation Strategy: Single Spec vs. Multi-Spec Organization**
   - **Decision**: Create one unified `system-capabilities` spec that brings all capabilities into a single requirements list
   - **Rationale**: Provides a complete, centralized view of the system's behavioral contract. Users or reviewers looking for system capabilities have one document to reference. This improves architectural clarity.
   - **Alternatives Considered**: 
     - Keeping six separate specs: Preserves modularity but disperses system understanding across documents
     - Creating nested specs under `system-capabilities/`: Adds organizational complexity without clarity benefit for a mature, stable system

2. **Requirement Organization: Capability-First Structure**
   - **Decision**: Organize consolidated requirements by capability domain (ingestion, search, MCP integration, agent skills, documentation isolation, PRD catalog) rather than technical concern
   - **Rationale**: Aligns with business/user-facing capability grouping. Makes it clear which requirements belong to which feature domain.
   - **Alternatives Considered**:
     - Layer-based organization (API/interfaces, data, services): Less clear for system users unfamiliar with architecture

3. **Scope of Consolidation: All Current Capabilities**
   - **Decision**: Include all twelve consolidated requirements representing the six source specs' full requirements
   - **Rationale**: Completeness ensures the spec is the authoritative reference for all system behavior
   - **Alternatives Considered**:
     - Summarizing only high-level capabilities: Loses testability and specificity needed for implementation contracts

4. **Traceability**
   - **Decision**: Preserve requirement names and scenario structure from source specs where possible to maintain traceability
   - **Rationale**: Allows future spec reviews to map back to original source documents. Supports incremental updates when individual capability specs need to evolve.
   - **Alternatives Considered**:
     - Renaming all requirements for consistency: Reduces traceability to source specs

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| Consolidation loses modularity and makes it harder to evolve individual capabilities independently | Maintain source spec files as reference; future changes to individual capabilities can be tracked separately and merged into this consolidated spec during archive. |
| Consolidated spec becomes large and difficult to navigate | Organize requirements by capability domain with clear section comments. Consumers can use document search and navigation. Future tooling could provide filtered views by capability. |
| Drift between consolidated spec and implementation as system evolves | Mark this spec for manual review at each significant change cycle. Establish a protocol: implementation changes → update source specs → regenerate consolidated spec. |
| Unclear which requirements are most critical for system operation | Each requirement includes scenario with explicit WHEN/THEN contract. Document separate "essential capabilities" reference if prioritization is needed later. |

## Migration Plan

**No implementation changes required.** The system already operates according to all specifications being consolidated.

**Steps:**
1. Create unified `system-capabilities` spec (this change)
2. Archive this change to generate the main spec in `openspec/specs/system-capabilities/spec.md`
3. Source specs (`rag-engine`, `hybrid-search`, etc.) remain available in `openspec/specs/` for reference and historical traceability
4. Document consolidation decision in project README or architecture guide (optional, out of scope for this change)

**No rollback needed:** This is a specification consolidation. No code deployment occurs. If the unified spec proves unwieldy, previous spec organization can be restored by re-establishing individual capability specs.

## Open Questions

- Should the archived `system-capabilities` spec note or link back to the six source specifications for historical traceability, or should consumers treat it as the definitive single source? (Deferrable: can be answered during archive and documented as an annotation or in a README)
- Future enhancement: Would a separate high-level "essential capabilities" document help prioritize which capabilities are core to the system vs. optional? (Out of scope: deferrable to a future change if needed)
