## 1. Project & Package Setup

- [x] 1.1 Create `rag-legado-skill/` directory layout with `mcp_server/`, `skill/`, `install.sh`, and configuration files
- [x] 1.2 Define Python dependencies (`requirements.txt` / `pyproject.toml`) for `tree-sitter`, `markdown-it-py`, `sentence-transformers`, `lancedb`, `rank-bm25`, and `mcp`

## 2. Core Ingestion & Vector Engine

- [x] 2.1 Implement repository file discovery in `mcp_server/ingest/parse_code.py` using `git ls-files` with `.gitignore`, `.ragignore`, extension, and size filters
- [x] 2.2 Implement AST-aware code chunking via `tree-sitter` for functions, classes, and methods preserving signature, docstrings, imports, line numbers, and commit metadata
- [x] 2.3 Implement markdown section chunking in `mcp_server/ingest/parse_docs.py` based on header hierarchy
- [x] 2.4 Implement local embedding generator in `mcp_server/index/embed.py` using `sentence-transformers`
- [x] 2.5 Implement LanceDB vector storage wrapper in `mcp_server/index/store.py`
- [x] 2.6 Create CLI verification scripts (`scripts/index_repo.py` and `scripts/search_test.py`) to test ingestion and vector search

## 3. Hybrid Search & Reranking

- [x] 3.1 Implement sparse BM25 indexing and keyword retrieval in `mcp_server/retrieve/hybrid_search.py` using `rank-bm25`
- [x] 3.2 Implement Reciprocal Rank Fusion (RRF) combining LanceDB dense vector results with BM25 keyword matching
- [x] 3.3 Implement local cross-encoder reranking in `mcp_server/retrieve/rerank.py` using `bge-reranker-base`

## 4. MCP Server Implementation

- [x] 4.1 Implement stdio MCP server entrypoint in `mcp_server/server.py` using the `mcp` Python SDK
- [x] 4.2 Expose `buscar_contexto(query, filtros)` tool returning reranked chunks with metadata
- [x] 4.3 Expose `reindexar(escopo)` tool supporting full or partial re-indexing
- [x] 4.4 Expose `status_indice()` tool returning chunk count, file count, and last indexed commit hash

## 5. Skills & Automation Setup

- [x] 5.1 Create Agent Skills compliant `skill/SKILL.md` instruction file
- [x] 5.2 Implement idempotent `install.sh` bootstrap installer that initializes the index, saves `.rag_state.json`, and registers MCP server with agents
- [x] 5.3 Implement `post-commit` and `post-merge` git hooks for fast incremental index updates based on git diffs

## 6. Documentation Skill Extension

- [x] 6.1 Implement `gerar_doc_modulo` MCP tool to generate structured module documentation from RAG context
- [x] 6.2 Implement document merge logic preserving manual edits while updating auto-generated sections under `docs/features/`
