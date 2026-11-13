## Purpose

Enables per-feature PRD generation for each business domain of the target application and creates a master module context document indexing all feature PRDs.

## ADDED Requirements

### Requirement: Individual Domain Feature PRD Generation
The system SHALL generate a separate, comprehensive PRD file in `docs/features/<feature-name>.md` for each identified domain feature of the target repository.

#### Scenario: Dedicated feature PRD output
- **WHEN** domain features are extracted from the target repository
- **THEN** each domain feature has a dedicated PRD containing its functional requirements, data models, APIs, and TDD specifications.

### Requirement: Master Module Context & Feature Index
The system SHALL maintain a master overview document (`docs/features/index.md`) detailing general module architecture and providing a table of contents / index to all feature PRDs.

#### Scenario: Master index generation
- **WHEN** all feature PRDs are generated or updated
- **THEN** the master document in `docs/features/index.md` is updated with high-level architecture notes and links to all generated feature PRDs.
