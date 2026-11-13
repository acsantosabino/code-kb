## Purpose

Combines dense vector similarity search with sparse BM25 keyword matching and cross-encoder reranking to deliver accurate relevant context chunks for queries.

## ADDED Requirements

### Requirement: Hybrid vector and BM25 search
The system SHALL retrieve relevant chunks by fusing top results from vector similarity search in LanceDB and keyword search via BM25 (`rank-bm25`).

#### Scenario: Execute hybrid retrieval query
- **WHEN** a natural language or code search query is received
- **THEN** the system retrieves top-k vector candidates and top-k BM25 candidates, fusing scores into a unified candidate list.

### Requirement: Cross-encoder reranking
The system SHALL re-score candidate chunks using a local cross-encoder model before returning top-n results.

#### Scenario: Rerank candidate chunks
- **WHEN** hybrid candidates are generated for a query
- **THEN** the local cross-encoder evaluates (query, chunk_content) pairs, sorts by relevance score, and returns the top-n reranked chunks.
