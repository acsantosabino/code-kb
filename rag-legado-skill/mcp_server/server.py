import json
import time
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from mcp_server.index.embed import generate_embeddings
from mcp_server.index.store import VectorStore
from mcp_server.ingest.discover import get_tracked_files
from mcp_server.ingest.parse_code import parse_code_file
from mcp_server.ingest.parse_docs import parse_markdown_file
from mcp_server.retrieve.bm25_index import BM25Index
from mcp_server.retrieve.hybrid_search import hybrid_search

mcp = FastMCP("rag-legado")

def get_repo_root() -> Path:
    return Path.cwd()


@mcp.tool()
def buscar_contexto(query: str, filtros: dict[str, Any] | None = None, top_k: int = 5) -> dict[str, Any]:
    """Search codebase RAG context using hybrid vector + BM25 retrieval and cross-encoder reranking."""
    repo_root = get_repo_root()
    try:
        results = hybrid_search(repo_root, query, top_k=top_k, filters=filtros)
        return {
            "resultados": results,
            "total_encontrado": len(results)
        }
    except Exception as e:
        return {
            "error": str(e),
            "resultados": [],
            "total_encontrado": 0
        }


@mcp.tool()
def reindexar(escopo: str | None = None) -> dict[str, Any]:
    """Trigger full or scope-specific reindexing of the repository codebase and documentation."""
    repo_root = get_repo_root()
    start_time = time.time()

    valid_files, ignored_report = get_tracked_files(repo_root)

    if escopo:
        escopo_str = str(escopo).strip().replace("\\", "/")
        valid_files = [f for f in valid_files if str(f.relative_to(repo_root)).replace("\\", "/").startswith(escopo_str)]

    all_chunks = []
    for f in valid_files:
        ext = f.suffix.lower()
        if ext in (".md", ".mdx", ".rst"):
            chunks = parse_markdown_file(f, repo_root)
        else:
            chunks = parse_code_file(f, repo_root)
        all_chunks.extend(chunks)

    if not all_chunks:
        return {
            "status": "warning",
            "message": "No files or chunks found for specified scope",
            "scope": escopo,
            "processed_chunks": 0
        }

    texts = [c["content"] for c in all_chunks]
    vectors = generate_embeddings(texts)

    store = VectorStore(repo_root)
    if escopo:
        for f in valid_files:
            rel_p = str(f.relative_to(repo_root))
            store.delete_chunks_by_file(rel_p)
    store.upsert_chunks(all_chunks, vectors)

    bm25 = BM25Index(repo_root)
    bm25.build_index(all_chunks)

    # Save state
    state_file = repo_root / ".rag_state.json"
    last_commit = "unknown"
    if all_chunks and "last_commit_hash" in all_chunks[0]:
        last_commit = all_chunks[0]["last_commit_hash"]
    
    state_data = {
        "last_indexed_commit": last_commit,
        "indexed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_files": len(valid_files),
        "total_chunks": len(all_chunks)
    }
    with open(state_file, "w", encoding="utf-8") as sf:
        json.dump(state_data, sf, indent=2)

    elapsed = time.time() - start_time
    return {
        "status": "success",
        "processed_files": len(valid_files),
        "processed_chunks": len(all_chunks),
        "elapsed_seconds": round(elapsed, 2),
        "scope": escopo or "full"
    }


@mcp.tool()
def status_indice() -> dict[str, Any]:
    """Inspect index health, chunk count, file count, and last indexed commit state."""
    repo_root = get_repo_root()
    store = VectorStore(repo_root)
    stats = store.get_stats()

    state_file = repo_root / ".rag_state.json"
    state_info = {}
    if state_file.exists():
        try:
            with open(state_file, "r", encoding="utf-8") as sf:
                state_info = json.load(sf)
        except Exception:
            pass

    return {
        "table_exists": stats.get("table_exists", False),
        "chunk_count": stats.get("chunk_count", 0),
        "file_count": stats.get("file_count", 0),
        "last_indexed_commit": state_info.get("last_indexed_commit", "none"),
        "indexed_at": state_info.get("indexed_at", "never")
    }


@mcp.tool()
def gerar_doc_modulo(caminho_ou_nome: str, modo: str = "criar") -> dict[str, Any]:
    """Generate or update structured module documentation under docs/features/ using RAG context."""
    repo_root = get_repo_root()
    from mcp_server.doc_generator import generate_module_doc
    return generate_module_doc(repo_root, caminho_ou_nome, modo=modo)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
