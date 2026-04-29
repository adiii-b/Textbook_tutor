"""
Loads the embedding index and retrieves the top-k chunks for a query.
"""

import pickle
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

INDEX_PATH = Path(__file__).parent.parent / "data" / "bm25_index.pkl"
MODEL_PATH = Path(__file__).parent.parent / "models" / "all-MiniLM-L6-v2"

_index_cache = None
_model = None


def reset_index():
    global _index_cache
    _index_cache = None


def _load_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(str(MODEL_PATH))
    return _model


def _load_index():
    global _index_cache
    if _index_cache is None:
        if not INDEX_PATH.exists():
            raise FileNotFoundError(
                "Index not found. Run retriever/index.py first."
            )
        with open(INDEX_PATH, "rb") as f:
            _index_cache = pickle.load(f)
    return _index_cache


SIMILARITY_THRESHOLD = 0.35


def retrieve(query: str, top_k: int = 1) -> list[dict]:
    data = _load_index()
    model = _load_model()

    chunk_embeddings = data["embeddings"]
    chunks = data["chunks"]

    query_embedding = model.encode(query, convert_to_numpy=True)

    norms = np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(query_embedding)
    scores = np.dot(chunk_embeddings, query_embedding) / norms

    top_indices = np.argsort(scores)[::-1][:top_k]

    if scores[top_indices[0]] < SIMILARITY_THRESHOLD:
        return []

    return [chunks[i] for i in top_indices]


if __name__ == "__main__":
    query = input("Enter search query: ")
    results = retrieve(query)
    for i, chunk in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(f"Chapter: {chunk.get('chapter')} | Section: {chunk.get('section')}")
        print(chunk["content"])
