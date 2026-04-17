"""
Loads the BM25 index and retrieves the top-k chunks for a query.
"""

import pickle
from pathlib import Path

INDEX_PATH = Path(__file__).parent.parent / "data" / "bm25_index.pkl"

_index_cache = None


def reset_index():
    global _index_cache
    _index_cache = None


def _load_index():
    global _index_cache
    if _index_cache is None:
        if not INDEX_PATH.exists():
            raise FileNotFoundError(
                "BM25 index not found. Run retriever/index.py first."
            )
        with open(INDEX_PATH, "rb") as f:
            _index_cache = pickle.load(f)
    return _index_cache


def tokenize(text: str) -> list[str]:
    return text.lower().split()


def retrieve(query: str, top_k: int = 2) -> list[dict]:
    data = _load_index()
    bm25 = data["bm25"]
    chunks = data["chunks"]

    scores = bm25.get_scores(tokenize(query))
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

    return [chunks[i] for i in top_indices]


if __name__ == "__main__":
    query = input("Enter search query: ")
    results = retrieve(query)
    for i, chunk in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(f"Chapter: {chunk.get('chapter')} | Section: {chunk.get('section')}")
        print(chunk["content"])
