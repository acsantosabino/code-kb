# Feature Doc Isolation

## Purpose

Ensures PRD document generation retrieves only target application code and segregates features cleanly without mixing in internal skill or meta documentation context.

## Requirements

### Requirement: Exclude Skill & Tooling Paths from Context Search
The system SHALL exclude internal skill directories (`.agent/`, `rag-legado-skill/`, `.claude/`, `docs/features/`) from RAG retrieval when generating PRDs for application modules.

#### Scenario: Target feature retrieval
- **WHEN** PRD generation is requested for a target module or feature
- **THEN** retrieved context chunks ONLY contain source files from the target application codebase.

### Requirement: Domain Feature Segregation
The system SHALL organize PRD documentation by distinct functional features and business domains rather than top-level tooling scripts.

#### Scenario: Segregated feature PRD output
- **WHEN** repository features are documented
- **THEN** each output file in `docs/features/<feature-slug>.md` represents a distinct domain feature with dedicated specs, architecture, and TDD scenarios.
