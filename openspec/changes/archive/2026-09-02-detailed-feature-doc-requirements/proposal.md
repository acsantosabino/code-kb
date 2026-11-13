## Why

The current feature documentation generation (`rag-legado-doc` / feature documentation generator) needs to produce comprehensive, structured, and detailed documentation for legacy and new features. Users require feature documentation to explicitly capture all project requirements, architectural components, dependencies, business rules, API/interface details, and test scenarios for each feature module.

## What Changes

- Enhance the feature documentation template and prompt structure in `rag-legado-doc` / documentation generation skill to enforce detailed section-by-section breakdown of project requirements for each feature following a standard PRD (Product Requirement Document) structure.
- Adopt standard PRD sections: Executive Summary & Objectives, User Stories/Use Cases, Functional Requirements, Non-Functional Requirements, Data Models & Architecture, Dependencies & Integrations, Edge Cases & Error Handling, TDD Test Suites (Unit, Integration, E2E acceptance criteria), and Full Reproduction Blueprint.
- Ensure feature PRD documentation contains sufficient technical detail, business logic specs, and implementation steps to allow faithful re-implementation/reproduction of the feature in a new project without relying on legacy code access.
- Implement segmented generation processing PRD content per context chunk (or per section) to prevent context truncation and ensure deep technical detail capture across extensive context datasets.
- Require all specifications to be strictly TDD-oriented, defining test-first scenarios, assertion conditions, input/output mocks, and expected test suite structures.
- Update `rag-legado-doc` skill rules and template schema to mandate standard PRD format when generating `docs/features/<feature>.md`.

## Capabilities

### Modified Capabilities
- `agent-skills`: Update the requirement specification for `rag-legado-doc` feature documentation generation to mandate detailed project requirements per feature module.

## Impact

- `rag-legado-skill/SKILL.md` or `rag-legado-doc` skill and templates.
- Generated documentation files in `docs/features/`.
- Downstream developers receiving comprehensive context and requirements for features.
