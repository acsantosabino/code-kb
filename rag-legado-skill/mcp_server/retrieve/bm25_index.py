import pickle
import re
from pathlib import Path
from typing import Any

from rank_bm25 import BM25Okapi


def tokenize(text: str) -> list[str]:
    # Extract alphanumeric tokens, lowercase
    tokens = re.findall(r"\w+", text.lower())
    return tokens


class BM25Index:
    def __init__(self, repo_root: Path | str):
        self.repo_root = Path(repo_root).resolve()
        self.index_file = self.repo_root / ".rag_index" / "bm25.pkl"
        self.bm25: BM25Okapi | None = None
        self.chunks: list[dict[str, Any]] = []
        self._load()

    def _load(self):
        if self.index_file.exists():
            try:
                with open(self.index_file, "rb") as f:
                    data = pickle.load(f)
                    self.chunks = data.get("chunks", [])
                    self.bm25 = data.get("bm25")
            except Exception:
                self.bm25 = None
                self.chunks = []

    def build_index(self, chunks: list[dict[str, Any]]):
        self.chunks = chunks
        corpus = []
        for c in chunks:
            text = f"{c.get('symbol_name', '')} {c.get('section_title', '')} {c.get('file_path', '')} {c.get('content', '')}"
            corpus.append(tokenize(text))

        if corpus:
            self.bm25 = BM25Okapi(corpus)
            self.index_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.index_file, "wb") as f:
                pickle.dump({"chunks": self.chunks, "bm25": self.bm25}, f)
        else:
            self.bm25 = None

    def search(self, query: str, top_k: int = 20) -> list[dict[str, Any]]:
        if not self.bm25 or not self.chunks:
            return []

        query_tokens = tokenize(query)
        scores = self.bm25.get_scores(query_tokens)
        
        # Zip scores with chunks
        scored_chunks = list(zip(scores, self.chunks))
        scored_chunks.sort(key=lambda x: x[0], reverse=True)

        results = []
        for score, chunk in scored_chunks[:top_k]:
            if score <= 0.0:
                continue
            item = dict(chunk)
            item["bm25_score"] = float(score)
            results.append(item)
        return results
