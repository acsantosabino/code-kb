## Purpose

Provides portable Agent Skills definition, automated idempotent repository setup (`install.sh`), and incremental git-hook updates to maintain index freshness.

## ADDED Requirements

### Requirement: Agent Skills standard packaging
The system SHALL provide an Agent Skills compliant `SKILL.md` that guides AI coding agents when and how to invoke the MCP server tools.

#### Scenario: Agent auto-invokes RAG skill
- **WHEN** an agent receives a prompt asking about system architecture, legacy code behavior, or un-opened modules
- **THEN** the agent follows the `SKILL.md` instructions to invoke `buscar_contexto`.

### Requirement: Automated bootstrap installer
The system SHALL provide an `install.sh` script that sets up dependencies, performs initial indexing, records `.rag_state.json`, and registers the MCP server in agent configurations.

#### Scenario: Run repository bootstrap installer
- **WHEN** `install.sh` is executed from the repository root
- **THEN** it installs python dependencies, builds the initial index, writes `.rag_state.json` containing the HEAD commit hash, and configures local AI agents.

### Requirement: Incremental git hook updates
The system SHALL provide `post-commit` and `post-merge` git hooks that detect modified files since `.rag_state.json` and incrementally update only changed chunks.

#### Scenario: Execute post-commit incremental sync
- **WHEN** a new commit is made in the repository
- **THEN** the git hook compares HEAD with `.rag_state.json`, re-indexes only altered files (`git diff --name-only`), and updates `.rag_state.json`.
