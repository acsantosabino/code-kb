# rag-engine Specification

## Purpose
Provides local-first repository ingestion, AST-aware code chunking, markdown section parsing, local vector embedding generation, and embedded LanceDB vector storage.
## Requirements
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

