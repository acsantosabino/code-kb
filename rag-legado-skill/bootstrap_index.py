import json
import subprocess
import sys
import time
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from mcp_server.index.embed import generate_embeddings
from mcp_server.index.store import VectorStore
from mcp_server.ingest.discover import get_tracked_files
from mcp_server.ingest.parse_code import parse_code_file
from mcp_server.ingest.parse_docs import parse_markdown_file
from mcp_server.retrieve.bm25_index import BM25Index


def get_git_head(repo_root: Path) -> str:
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


def run_bootstrap(repo_path: Path):
    repo_path = repo_path.resolve()
    print(f"=== Starting RAG Bootstrap Indexing: {repo_path.name} ===")
    start_time = time.time()

    valid_files, ignored_report = get_tracked_files(repo_path)
    print(f"Discovered {len(valid_files)} supported files ({len(ignored_report)} ignored).")

    all_chunks = []
    for idx, f in enumerate(valid_files, start=1):
        if idx % 20 == 0 or idx == len(valid_files):
            print(f"Parsing files... ({idx}/{len(valid_files)})")
        ext = f.suffix.lower()
        if ext in (".md", ".mdx", ".rst"):
            chunks = parse_markdown_file(f, repo_path)
        else:
            chunks = parse_code_file(f, repo_path)
        all_chunks.extend(chunks)

    print(f"Extracted {len(all_chunks)} structural chunks.")

    if not all_chunks:
        print("Warning: No content chunks extracted.")
        return

    print("Generating embeddings...")
    texts = [c["content"] for c in all_chunks]
    vectors = generate_embeddings(texts)

    print("Writing LanceDB vector store...")
    store = VectorStore(repo_path)
    store.clear_index()
    store.upsert_chunks(all_chunks, vectors)

    print("Building BM25 keyword index...")
    bm25 = BM25Index(repo_path)
    bm25.build_index(all_chunks)

    head_hash = get_git_head(repo_path)
    state_file = repo_path / ".rag_state.json"
    state_data = {
        "last_indexed_commit": head_hash,
        "indexed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_files": len(valid_files),
        "total_chunks": len(all_chunks)
    }

    with open(state_file, "w", encoding="utf-8") as sf:
        json.dump(state_data, sf, indent=2)

    elapsed = time.time() - start_time
    print(f"\n✅ Bootstrap completed successfully in {elapsed:.2f}s!")
    print(f"   Indexed Files : {len(valid_files)}")
    print(f"   Total Chunks  : {len(all_chunks)}")
    print(f"   HEAD Commit   : {head_hash[:7]}")


if __name__ == "__main__":
    repo_arg = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    run_bootstrap(repo_arg)
