# system-capabilities Specification

## Purpose

Consolidates the complete set of operational and architectural capabilities of the local RAG/Legacy Documentation ecosystem, providing a centralized specification for repository ingestion, hybrid search, MCP server integration, AI agent skills, documentation isolation, and feature PRD cataloging.

## ADDED Requirements

### Requirement: Repository file discovery with git tracking and ignore rules
The system SHALL discover source code and documentation files using `git ls-files` while honoring `.gitignore`, `.ragignore`, file extension filters, and file size limits.

#### Scenario: Discover tracked files respecting filters
- **WHEN** ingestion is initiated on a git repository
- **THEN** the system returns all tracked files matching supported extensions (`.py`, `.js`, `.ts`, `.java`, `.go`, `.rb`, `.php`, `.md`, `.mdx`, `.rst`), excluding any files matching `.ragignore` or exceeding 1MB.

### Requirement: AST-aware code chunking
The system SHALL parse source code files using `tree-sitter` and produce chunks corresponding to logical code units (functions, classes, methods) with surrounding docstrings/comments and metadata.

#### Scenario: Parse code file into structural chunks
- **WHEN** a source code file is chunked by the ingestion pipeline
- **THEN** each chunk contains the symbol signature, body, docstring/comments, line numbers, file path, language, deterministic `chunk_id`, and last git commit metadata.

### Requirement: Markdown section chunking
The system SHALL parse Markdown documentation files into structural chunks based on header hierarchy.

#### Scenario: Parse markdown document by headers
- **WHEN** a Markdown file is chunked
- **THEN** each chunk represents a header section with section title, level, file path, and text content.

### Requirement: Local vector embedding and LanceDB storage
The system SHALL compute embeddings using local sentence-transformer models without external API calls and persist vectors and metadata into an embedded LanceDB database.

#### Scenario: Compute embeddings and persist to LanceDB
- **WHEN** chunks are passed to the embedding module
- **THEN** local embeddings are generated and stored in a local LanceDB table along with chunk metadata.

### Requirement: Hybrid search with BM25 and vector similarity
The system SHALL support hybrid search combining BM25 full-text matching with dense vector similarity, allowing users to query via natural language or keywords.

#### Scenario: Execute hybrid search query
- **WHEN** a user submits a search query
- **THEN** the system returns reranked results combining BM25 keyword relevance and vector semantic similarity, ordered by hybrid score.

### Requirement: Result reranking with context preservation
The system SHALL rerank search results using learned-to-rank algorithms to improve relevance while preserving complete chunk metadata (file path, line numbers, symbol name, commit info).

#### Scenario: Rerank hybrid search results
- **WHEN** hybrid search returns candidates
- **THEN** results are reranked by relevance score and returned with full metadata for source location and context identification.

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

### Requirement: Agent skill integration for documentation queries
The system SHALL provide agent skills that enable AI agents to access repository context via structured interfaces for documentation queries and code exploration.

#### Scenario: Use agent skill to search documentation
- **WHEN** an AI agent invokes the documentation query skill
- **THEN** the agent receives search results with relevant documentation chunks and metadata for context-aware responses.

### Requirement: Feature-level documentation isolation
The system SHALL support isolating documentation and code context by feature boundaries, allowing per-feature PRD and documentation retrieval.

#### Scenario: Query documentation for specific feature
- **WHEN** a user queries context for a specific feature identifier
- **THEN** the system returns documentation and code chunks relevant only to that feature, excluding other features' context.

### Requirement: Per-feature PRD catalog
The system SHALL maintain and expose a catalog of Product Requirements Documents (PRDs) organized by feature, enabling feature-specific documentation retrieval and context building.

#### Scenario: Retrieve PRD for a feature
- **WHEN** a user requests the PRD for a specific feature
- **THEN** the system returns the formatted PRD document with feature requirements, specifications, and impact information.

### Requirement: Incremental index updates
The system SHALL support incremental indexing triggered by post-commit hooks, updating the vector store with only changed files rather than full re-indexing.

#### Scenario: Auto-update index on repository change
- **WHEN** files are committed to the repository
- **THEN** post-commit hooks trigger incremental indexing, adding/updating only changed chunks in the vector store without full re-indexing.

### Requirement: Index health monitoring and recovery
The system SHALL provide health checks for index consistency and recovery mechanisms for corrupted or stale indexes.

#### Scenario: Monitor and recover index
- **WHEN** health checks are run
- **THEN** the system validates index integrity, reports stale chunks, and provides recovery mechanisms to rebuild corrupted sections.
