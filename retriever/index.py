"""
Builds and saves the BM25 index from textbook.json chunks.
Run this once after updating textbook.json.
"""

import json
import pickle
from pathlib import Path
from rank_bm25 import BM25Okapi

DATA_PATH = Path(__file__).parent.parent / "data" / "textbook.json"
INDEX_PATH = Path(__file__).parent.parent / "data" / "bm25_index.pkl"


def tokenize(text: str) -> list[str]:
    return text.lower().split()


def build_index():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    if not chunks:
        print("textbook.json is empty. Add chunks before building the index.")
        return

    corpus = [tokenize(chunk["content"]) for chunk in chunks]
    bm25 = BM25Okapi(corpus)

    with open(INDEX_PATH, "wb") as f:
        pickle.dump({"bm25": bm25, "chunks": chunks}, f)

    print(f"Index built with {len(chunks)} chunks → saved to {INDEX_PATH}")


if __name__ == "__main__":
    build_index()
