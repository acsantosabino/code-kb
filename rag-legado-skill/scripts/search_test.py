import argparse
import json
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp_server.index.embed import generate_embeddings
from mcp_server.index.store import VectorStore
from mcp_server.retrieve.hybrid_search import hybrid_search


def search_test(repo_path: Path, query: str, top_k: int = 5, mode: str = "hybrid"):
    repo_path = repo_path.resolve()
    print(f"\n--- Search Results [{mode.upper()}] for Query: '{query}' (top-{top_k}) ---")

    if mode == "hybrid":
        results = hybrid_search(repo_path, query, top_k=top_k)
    else:
        store = VectorStore(repo_path)
        vecs = generate_embeddings([query])
        results = store.search_vector(vecs[0], top_k=top_k) if vecs else []

    for idx, res in enumerate(results, start=1):
        score_str = f"Rerank: {res.get('rerank_score', 0.0):.4f} (RRF: {res.get('rrf_score', 0.0):.4f})" if mode == "hybrid" else f"Score: {res.get('score', 0.0):.4f}"
        print(f"\n[{idx}] {score_str} | File: {res.get('file_path')} (L{res.get('start_line')}-L{res.get('end_line')})")
        print(f"    Symbol/Title: {res.get('symbol_name') or res.get('section_title')}")
        snippet = res.get('content', '').strip().replace('\n', ' ')
        if len(snippet) > 120:
            snippet = snippet[:117] + "..."
        print(f"    Content: {snippet}")


def main():
    parser = argparse.ArgumentParser(description="Test RAG search over local index.")
    parser.add_argument("--repo-path", type=str, default=".", help="Path to repository root")
    parser.add_argument("--query", type=str, required=True, help="Search query")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results")
    parser.add_argument("--mode", type=str, default="hybrid", choices=["hybrid", "vector"], help="Search mode")
    args = parser.parse_args()
    
    search_test(Path(args.repo_path), args.query, args.top_k, args.mode)


if __name__ == "__main__":
    main()
