## Why

Monolithic codebase developers working with AI coding tools (Claude Code, Antigravity, GitHub Copilot) face context loss regarding repository history, architectural decisions, and legacy module behaviors. Today, this knowledge exists only in developers' heads or post-mortem notes.

This change introduces a portable, local-first RAG (Retrieval-Augmented Generation) knowledge base and agent skills package (`code-kb`). It enables coding agents to search structural code and documentation context locally without relying on paid external APIs or leaking code outside the user's machine.

## What Changes

- **Core RAG Engine**: Build AST-aware code chunking via `tree-sitter` and section-based markdown chunking, local embedding generation, and LanceDB embedded vector storage.
- **Hybrid Search & Reranking**: Implement hybrid retrieval fusing LanceDB vector search with BM25 keyword matching (`rank-bm25`) and local cross-encoder reranking (`bge-reranker-base`).
- **MCP Server**: Create a local Model Context Protocol server exposing `buscar_contexto`, `reindexar`, and `status_indice` tools for AI agent invocation.
- **Skills & Bootstrap Automation**: Create portable Agent Skills (`SKILL.md`), an idempotent `install.sh` installer, and git hooks (`post-commit`/`post-merge`) for incremental updates based on `.rag_state.json`.

## Capabilities

### New Capabilities
- `rag-engine`: Ingestion pipeline, AST code chunking, markdown chunking, local embeddings, and LanceDB vector store.
- `hybrid-search`: Dense vector search combined with BM25 keyword search and cross-encoder reranking.
- `mcp-server`: MCP server exposing local RAG tools to AI coding assistants.
- `agent-skills`: Agent skills packaging, repository bootstrap script (`install.sh`), and incremental update git hooks.

### Modified Capabilities

*(None - initial implementation of the knowledge base)*

## Impact

- **Affected Components**: New Python package under `mcp_server/`, skills under `skill/`, install scripts `install.sh`, and configuration files (`.ragignore`, `.rag_state.json`).
- **Dependencies**: Python dependencies (`tree-sitter`, `markdown-it-py`, `sentence-transformers`, `lancedb`, `rank-bm25`, `mcp`).
- **APIs**: Exposes standard MCP tools over stdio.
