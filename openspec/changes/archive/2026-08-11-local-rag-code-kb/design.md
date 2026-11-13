## Context

See `proposal.md` for project background and motivation. This design covers the technical architecture and component breakdown for `code-kb`—a local-first, portable RAG package and agent skills integration.

## Goals / Non-Goals

**Goals:**
- Provide a local-first Python implementation without external framework bloat (no LangChain / LlamaIndex).
- Ensure fast, AST-aware chunking for code (`tree-sitter`) and section chunking for markdown docs (`markdown-it-py`).
- Implement hybrid search (dense LanceDB vector search + sparse BM25) and local cross-encoder reranking.
- Expose tools via MCP stdio protocol for seamless integration into Claude Code, Antigravity, and GitHub Copilot.
- Package as an easy-to-install, portable script (`install.sh`) with git hook incremental syncing.

**Non-Goals:**
- Multi-repository indexing in v1.
- Cloud SaaS backends or paid third-party API dependencies.
- General enterprise search (Slack, Jira, etc.).

## Architecture & Directory Structure

```
rag-legado-skill/
├── mcp_server/
│   ├── server.py            # MCP stdio tool definitions
│   ├── ingest/
│   │   ├── parse_code.py    # AST code chunking via tree-sitter
│   │   └── parse_docs.py    # Markdown section chunking
│   ├── index/
│   │   ├── embed.py         # Local sentence-transformers embeddings
│   │   └── store.py         # LanceDB wrapper
│   └── retrieve/
│       ├── hybrid_search.py # Vector + BM25 fusion
│       └── rerank.py        # Local cross-encoder reranking
├── skill/
│   ├── SKILL.md             # Agent Skills instruction
│   └── references/
│       └── metadata_schema.md
├── install.sh               # Bootstrap installer & registration
├── bootstrap_index.py        # Repository initial indexer
└── README.md
```

## Decisions

### Decision 1: Lightweight Custom RAG Stack vs. LangChain/LlamaIndex
- **Rationale**: Third-party RAG frameworks introduce heavy dependency trees and breaking API updates. Writing a clean, direct pipeline using `sentence-transformers`, `LanceDB`, `tree-sitter`, and `mcp` SDK ensures stability, fast startup times, and full control over memory footprint.

### Decision 2: Embedded LanceDB Vector Storage
- **Rationale**: LanceDB operates as an embedded vector database writing directly to local disk storage (Parquet-backed), eliminating the need to run Docker containers or background daemon processes like Qdrant or Milvus.

### Decision 3: AST-Aware Chunking via `tree-sitter`
- **Rationale**: Naive text or fixed-token line splitters break code context (e.g., splitting a function across two chunks). `tree-sitter` provides exact AST parsing per function/class/method, preserving signature, docstrings, and exact line boundaries.

### Decision 4: Hybrid Search + Local Cross-Encoder Reranking
- **Rationale**: Dense vector retrieval excels at semantic intent, while sparse BM25 excels at exact symbol names and error codes. Combining both via Reciprocal Rank Fusion (RRF) and reranking top candidates with a local cross-encoder (`bge-reranker-base`) yields optimal precision.

### Decision 5: Git-Based Incremental Indexing via `.rag_state.json`
- **Rationale**: Full re-indexing on every commit is wasteful. Saving the index commit hash in `.rag_state.json` allows git hooks (`post-commit`, `post-merge`) to query `git diff --name-only <last_commit> HEAD` and update only modified/added files in seconds.

## Risks / Trade-offs

- **[First-run embedding model download delay]** → `install.sh` displays a progress indicator and downloads local weights once into `~/.cache/huggingface/`.
- **[Memory usage during full repo indexing]** → Batched processing of chunks (e.g., batches of 64 chunks) to cap peak RAM usage under 1.5GB on standard dev laptops.
- **[Stale vector index]** → Automatic installation of git `post-commit` and `post-merge` hooks during `install.sh` ensures incremental sync on every commit.
