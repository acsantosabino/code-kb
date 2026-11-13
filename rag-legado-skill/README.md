# RAG Legado Skill (`code-kb`)

Local-first, portable RAG (Retrieval-Augmented Generation) knowledge base and agent skills for codebase documentation and architectural intelligence.

## Features
- **AST-Aware Code Chunking**: Powered by `tree-sitter` for structured function and class parsing.
- **Section-Based Markdown Parsing**: Hierarchical document chunking with `markdown-it-py`.
- **Hybrid Retrieval**: Dense LanceDB vector search fused with BM25 keyword search using RRF (Reciprocal Rank Fusion).
- **Cross-Encoder Reranking**: Re-scoring top candidates with local cross-encoder models.
- **MCP Server Protocol**: Stdio interface exposing RAG tools (`buscar_contexto`, `reindexar`, `status_indice`, `gerar_doc_modulo`) to AI assistants.
- **Incremental Git Sync**: Post-commit and post-merge hooks for fast incremental re-indexing based on git diffs.

## Installation
```bash
./install.sh
```
