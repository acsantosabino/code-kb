from pathlib import Path
from typing import Any

import lancedb
import pyarrow as pa


def get_db_path(repo_root: Path | str) -> Path:
    p = Path(repo_root) / ".rag_index" / "lancedb"
    p.mkdir(parents=True, exist_ok=True)
    return p


class VectorStore:
    TABLE_NAME = "chunks"

    def __init__(self, repo_root: Path | str):
        self.repo_root = Path(repo_root).resolve()
        self.db_path = get_db_path(self.repo_root)
        self.db = lancedb.connect(str(self.db_path))

    def _get_schema(self, dim: int = 384) -> pa.Schema:
        return pa.schema([
            ("vector", pa.list_(pa.float32(), dim)),
            ("chunk_id", pa.string()),
            ("file_path", pa.string()),
            ("language", pa.string()),
            ("symbol_name", pa.string()),
            ("symbol_type", pa.string()),
            ("section_title", pa.string()),
            ("header_level", pa.int32()),
            ("start_line", pa.int32()),
            ("end_line", pa.int32()),
            ("last_commit_hash", pa.string()),
            ("last_commit_date", pa.string()),
            ("last_commit_author", pa.string()),
            ("chunk_type", pa.string()),
            ("content", pa.string()),
        ])

    def get_table(self, dim: int = 384):
        if self.TABLE_NAME in self.db.table_names():
            return self.db.open_table(self.TABLE_NAME)
        else:
            schema = self._get_schema(dim)
            return self.db.create_table(self.TABLE_NAME, schema=schema)

    def upsert_chunks(self, chunks: list[dict[str, Any]], vectors: list[list[float]]):
        if not chunks:
            return

        dim = len(vectors[0]) if vectors else 384
        records = []

        for c, vec in zip(chunks, vectors):
            records.append({
                "vector": [float(x) for x in vec],
                "chunk_id": str(c.get("chunk_id", "")),
                "file_path": str(c.get("file_path", "")),
                "language": str(c.get("language", "")),
                "symbol_name": str(c.get("symbol_name", "")),
                "symbol_type": str(c.get("symbol_type", "")),
                "section_title": str(c.get("section_title", "")),
                "header_level": int(c.get("header_level", 0)),
                "start_line": int(c.get("start_line", 1)),
                "end_line": int(c.get("end_line", 1)),
                "last_commit_hash": str(c.get("last_commit_hash", "")),
                "last_commit_date": str(c.get("last_commit_date", "")),
                "last_commit_author": str(c.get("last_commit_author", "")),
                "chunk_type": str(c.get("chunk_type", "code")),
                "content": str(c.get("content", ""))
            })

        table = self.get_table(dim)
        # Delete existing chunks with matching IDs to enforce deterministic upsert
        chunk_ids = [r["chunk_id"] for r in records]
        if chunk_ids:
            formatted_ids = ", ".join(f"'{cid}'" for cid in chunk_ids)
            try:
                table.delete(f"chunk_id IN ({formatted_ids})")
            except Exception:
                pass

        table.add(records)

    def delete_chunks_by_file(self, file_path: str):
        if self.TABLE_NAME in self.db.table_names():
            table = self.db.open_table(self.TABLE_NAME)
            try:
                table.delete(f"file_path = '{file_path}'")
            except Exception:
                pass

    def search_vector(
        self,
        query_vector: list[float],
        top_k: int = 20,
        filters: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        if self.TABLE_NAME not in self.db.table_names():
            return []

        table = self.db.open_table(self.TABLE_NAME)
        query = table.search(query_vector).limit(top_k)

        if filters:
            conditions = []
            if "chunk_type" in filters and filters["chunk_type"]:
                conditions.append(f"chunk_type = '{filters['chunk_type']}'")
            if "language" in filters and filters["language"]:
                conditions.append(f"language = '{filters['language']}'")
            if "file_path_prefix" in filters and filters["file_path_prefix"]:
                prefix = filters["file_path_prefix"]
                conditions.append(f"file_path LIKE '{prefix}%'")

            if conditions:
                query = query.where(" AND ".join(conditions))

        results = query.to_list()
        formatted = []
        for r in results:
            item = dict(r)
            score = float(1.0 / (1.0 + item.get("_distance", 0.0)))
            item["score"] = score
            formatted.append(item)
        return formatted

    def get_all_chunks(self) -> list[dict[str, Any]]:
        if self.TABLE_NAME not in self.db.table_names():
            return []
        table = self.db.open_table(self.TABLE_NAME)
        return table.search().limit(100000).to_list()

    def get_stats(self) -> dict[str, Any]:
        if self.TABLE_NAME not in self.db.table_names():
            return {
                "chunk_count": 0,
                "file_count": 0,
                "table_exists": False
            }
        table = self.db.open_table(self.TABLE_NAME)
        all_records = table.search().limit(100000).to_list()
        files = {r["file_path"] for r in all_records if "file_path" in r}
        return {
            "chunk_count": len(all_records),
            "file_count": len(files),
            "table_exists": True
        }

    def clear_index(self):
        if self.TABLE_NAME in self.db.table_names():
            self.db.drop_table(self.TABLE_NAME)
