import json
import subprocess
import time
from pathlib import Path

from mcp_server.index.embed import generate_embeddings
from mcp_server.index.store import VectorStore
from mcp_server.ingest.discover import get_tracked_files
from mcp_server.ingest.parse_code import parse_code_file
from mcp_server.ingest.parse_docs import parse_markdown_file
from mcp_server.retrieve.bm25_index import BM25Index


def get_current_head(repo_root: Path) -> str:
    try:
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception:
        return "unknown"


def run_incremental_update(repo_root: Path | str):
    repo_path = Path(repo_root).resolve()
    state_file = repo_path / ".rag_state.json"

    if not state_file.exists():
        print("No .rag_state.json found. Running full re-index.")
        from mcp_server.server import reindexar
        return reindexar()

    with open(state_file, "r", encoding="utf-8") as sf:
        state_data = json.load(sf)

    last_commit = state_data.get("last_indexed_commit")
    current_head = get_current_head(repo_path)

    if not last_commit or last_commit == "unknown" or last_commit == current_head:
        print("Index already up to date with HEAD.")
        return {"status": "up_to_date", "head": current_head}

    try:
        res = subprocess.run(
            ["git", "diff", "--name-only", last_commit, current_head],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            check=True
        )
        changed_files = [line.strip() for line in res.stdout.splitlines() if line.strip()]
    except Exception as e:
        print(f"Error running git diff: {e}. Falling back to full re-index.")
        from mcp_server.server import reindexar
        return reindexar()

    if not changed_files:
        print("No file changes detected since last commit.")
        state_data["last_indexed_commit"] = current_head
        with open(state_file, "w", encoding="utf-8") as sf:
            json.dump(state_data, sf, indent=2)
        return {"status": "up_to_date", "head": current_head}

    store = VectorStore(repo_path)

    new_chunks_to_upsert = []
    for rel_str in changed_files:
        abs_p = repo_path / rel_str
        # Always delete old chunks for this file
        store.delete_chunks_by_file(rel_str)

        if abs_p.exists() and abs_p.is_file():
            ext = abs_p.suffix.lower()
            if ext in (".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".rb", ".php"):
                chunks = parse_code_file(abs_p, repo_path)
                new_chunks_to_upsert.extend(chunks)
            elif ext in (".md", ".mdx", ".rst"):
                chunks = parse_markdown_file(abs_p, repo_path)
                new_chunks_to_upsert.extend(chunks)

    if new_chunks_to_upsert:
        texts = [c["content"] for c in new_chunks_to_upsert]
        vectors = generate_embeddings(texts)
        store.upsert_chunks(new_chunks_to_upsert, vectors)

    # Rebuild BM25 index with current all_chunks
    all_chunks = store.get_all_chunks()
    bm25 = BM25Index(repo_path)
    bm25.build_index(all_chunks)

    stats = store.get_stats()
    state_data["last_indexed_commit"] = current_head
    state_data["indexed_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    state_data["total_files"] = stats.get("file_count", 0)
    state_data["total_chunks"] = stats.get("chunk_count", 0)

    with open(state_file, "w", encoding="utf-8") as sf:
        json.dump(state_data, sf, indent=2)

    print(f"Incremental update complete for {len(changed_files)} changed files. New HEAD: {current_head[:7]}")
    return {
        "status": "success",
        "changed_files_count": len(changed_files),
        "new_head": current_head
    }


if __name__ == "__main__":
    run_incremental_update(Path.cwd())
