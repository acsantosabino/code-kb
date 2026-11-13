## Purpose

Exposes Model Context Protocol (MCP) tools over stdio, enabling external AI coding assistants (Claude Code, Antigravity, GitHub Copilot) to query context, trigger reindexing, and inspect index health.

## ADDED Requirements

### Requirement: MCP tool context search
The system SHALL expose an MCP tool `buscar_contexto(query: str, filtros?: dict)` returning reranked context chunks with complete metadata.

#### Scenario: Query context via MCP tool
- **WHEN** an AI assistant calls `buscar_contexto` with a query
- **THEN** the MCP server executes hybrid search and reranking, returning matching code/doc chunks formatted with file path, line numbers, symbol name, and last commit details.

### Requirement: MCP tool reindexing
The system SHALL expose an MCP tool `reindexar(escopo?: str)` allowing full or partial re-indexing of repository files.

#### Scenario: Trigger reindexing via MCP tool
- **WHEN** an AI assistant calls `reindexar`
- **THEN** the server re-runs ingestion for the specified scope and updates the local vector store.

### Requirement: MCP tool status inspection
The system SHALL expose an MCP tool `status_indice()` returning health metrics of the vector index.

#### Scenario: Check index status via MCP tool
- **WHEN** `status_indice` is invoked
- **THEN** the server returns total chunk count, indexed file count, last indexed commit hash, and index last-updated timestamp.
