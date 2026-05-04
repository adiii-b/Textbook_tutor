import pickle
import numpy as np
from pathlib import Path
from retriever.embedder import encode

INDEX_PATH = Path(__file__).parent.parent / "data" / "bm25_index.pkl"

_index_cache = None


def reset_index():
    global _index_cache
    _index_cache = None


def _load_index():
    global _index_cache
    if _index_cache is None:
        if not INDEX_PATH.exists():
            raise FileNotFoundError("Index not found. Run retriever/index.py first.")
        with open(INDEX_PATH, "rb") as f:
            _index_cache = pickle.load(f)
    return _index_cache


SIMILARITY_THRESHOLD = 0.35


def retrieve(query: str, top_k: int = 1) -> list[dict]:
    data = _load_index()
    chunk_embeddings = data["embeddings"]
    chunks = data["chunks"]

    query_embedding = encode(query)[0]

    norms = np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(query_embedding)
    scores = np.dot(chunk_embeddings, query_embedding) / np.maximum(norms, 1e-9)

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
