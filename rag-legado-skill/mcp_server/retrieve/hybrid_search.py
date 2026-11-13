from pathlib import Path
from typing import Any

from mcp_server.index.embed import generate_embeddings
from mcp_server.index.store import VectorStore
from mcp_server.retrieve.bm25_index import BM25Index
from mcp_server.retrieve.rerank import rerank_chunks


def rrf_fusion(
    dense_results: list[dict[str, Any]],
    sparse_results: list[dict[str, Any]],
    k: int = 60,
    top_n: int = 20
) -> list[dict[str, Any]]:
    scores: dict[str, float] = {}
    chunk_map: dict[str, dict[str, Any]] = {}

    # Dense scores
    for rank, item in enumerate(dense_results, start=1):
        cid = item.get("chunk_id")
        if not cid:
            continue
        chunk_map[cid] = item
        scores[cid] = scores.get(cid, 0.0) + (1.0 / (k + rank))

    # Sparse scores
    for rank, item in enumerate(sparse_results, start=1):
        cid = item.get("chunk_id")
        if not cid:
            continue
        if cid not in chunk_map:
            chunk_map[cid] = item
        scores[cid] = scores.get(cid, 0.0) + (1.0 / (k + rank))

    sorted_cids = sorted(scores.keys(), key=lambda cid: scores[cid], reverse=True)

    candidates = []
    for cid in sorted_cids[:top_n]:
        chunk = dict(chunk_map[cid])
        chunk["rrf_score"] = scores[cid]
        candidates.append(chunk)

    return candidates


def hybrid_search(
    repo_root: Path | str,
    query: str,
    top_k: int = 5,
    filters: dict[str, Any] | None = None,
    rrf_k: int = 60,
    candidate_limit: int = 20
) -> list[dict[str, Any]]:
    repo_path = Path(repo_root).resolve()
    
    # 1. Vector dense search
    store = VectorStore(repo_path)
    vecs = generate_embeddings([query])
    dense_results = store.search_vector(vecs[0], top_k=candidate_limit, filters=filters) if vecs else []

    # 2. BM25 sparse search
    bm25_idx = BM25Index(repo_path)
    sparse_results = bm25_idx.search(query, top_k=candidate_limit)

    # Filter sparse results if filters are provided
    if filters and sparse_results:
        filtered_sparse = []
        for item in sparse_results:
            if "chunk_type" in filters and filters["chunk_type"] and item.get("chunk_type") != filters["chunk_type"]:
                continue
            if "language" in filters and filters["language"] and item.get("language") != filters["language"]:
                continue
            if "file_path_prefix" in filters and filters["file_path_prefix"] and not item.get("file_path", "").startswith(filters["file_path_prefix"]):
                continue
            filtered_sparse.append(item)
        sparse_results = filtered_sparse

    # 3. RRF Fusion
    candidates = rrf_fusion(dense_results, sparse_results, k=rrf_k, top_n=candidate_limit)

    # 4. Reranking
    final_results = rerank_chunks(query, candidates, top_k=top_k)
    return final_results
