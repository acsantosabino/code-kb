from typing import Any

_model_instance = None


def get_embedding_model(model_name: str = "all-MiniLM-L6-v2"):
    global _model_instance
    if _model_instance is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model_instance = SentenceTransformer(model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to load sentence-transformers model '{model_name}': {e}")
    return _model_instance


def generate_embeddings(
    texts: list[str],
    model_name: str = "all-MiniLM-L6-v2",
    batch_size: int = 32
) -> list[list[float]]:
    if not texts:
        return []
    model = get_embedding_model(model_name)
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=False,
        convert_to_numpy=True
    )
    return embeddings.tolist()
