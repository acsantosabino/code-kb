import argparse
import sys
import time
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp_server.index.embed import generate_embeddings
from mcp_server.index.store import VectorStore
from mcp_server.ingest.discover import get_tracked_files
from mcp_server.ingest.parse_code import parse_code_file
from mcp_server.ingest.parse_docs import parse_markdown_file


def index_repository(repo_path: Path):
    repo_path = repo_path.resolve()
    print(f"Indexing repository at: {repo_path}")
    start_time = time.time()

    valid_files, ignored_report = get_tracked_files(repo_path)
    print(f"Discovered {len(valid_files)} supported files ({len(ignored_report)} ignored).")

    all_chunks = []
    for f in valid_files:
        ext = f.suffix.lower()
        if ext in (".md", ".mdx", ".rst"):
            chunks = parse_markdown_file(f, repo_path)
        else:
            chunks = parse_code_file(f, repo_path)
        all_chunks.extend(chunks)

    print(f"Extracted {len(all_chunks)} structural chunks.")

    if not all_chunks:
        print("No chunks found to index.")
        return

    print("Generating embeddings...")
    texts = [c["content"] for c in all_chunks]
    vectors = generate_embeddings(texts)

    print("Persisting to LanceDB...")
    store = VectorStore(repo_path)
    store.upsert_chunks(all_chunks, vectors)

    print("Building BM25 index...")
    from mcp_server.retrieve.bm25_index import BM25Index
    bm25 = BM25Index(repo_path)
    bm25.build_index(all_chunks)

    elapsed = time.time() - start_time
    stats = store.get_stats()
    print("\n--- Indexing Report ---")
    print(f"Indexed files : {stats['file_count']}")
    print(f"Total chunks  : {stats['chunk_count']}")
    print(f"Time elapsed  : {elapsed:.2f}s")
    if ignored_report:
        print(f"\nIgnored files summary ({len(ignored_report)} items):")
        for item in ignored_report[:10]:
            print(f"  - {item['file_path']}: {item['reason']}")
        if len(ignored_report) > 10:
            print(f"  ... and {len(ignored_report) - 10} more.")


def main():
    parser = argparse.ArgumentParser(description="Index repository into local RAG vector store.")
    parser.add_argument("--repo-path", type=str, default=".", help="Path to repository root")
    args = parser.parse_args()
    index_repository(Path(args.repo_path))


if __name__ == "__main__":
    main()
