from typing import Any

_reranker_instance = None


def get_reranker(model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
    global _reranker_instance
    if _reranker_instance is None:
        try:
            from sentence_transformers import CrossEncoder
            _reranker_instance = CrossEncoder(model_name)
        except Exception as e:
            _reranker_instance = None
    return _reranker_instance


def rerank_chunks(
    query: str,
    chunks: list[dict[str, Any]],
    top_k: int = 5,
    model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
) -> list[dict[str, Any]]:
    if not chunks:
        return []

    try:
        reranker = get_reranker(model_name)
        if reranker is not None:
            pairs = [[query, c.get("content", "")] for c in chunks]
            scores = reranker.predict(pairs)

            for chunk, score in zip(chunks, scores):
                chunk["rerank_score"] = float(score)

            chunks.sort(key=lambda x: x.get("rerank_score", 0.0), reverse=True)
            return chunks[:top_k]
    except Exception:
        pass

    # Fallback: keep current order
    return chunks[:top_k]
