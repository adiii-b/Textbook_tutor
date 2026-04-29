"""
Builds and saves the embedding index from textbook.json chunks.
Run this once after updating textbook.json.
"""

import json
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer

DATA_PATH = Path(__file__).parent.parent / "data" / "textbook.json"
INDEX_PATH = Path(__file__).parent.parent / "data" / "bm25_index.pkl"
MODEL_PATH = Path(__file__).parent.parent / "models" / "all-MiniLM-L6-v2"


def build_index():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    if not chunks:
        print("textbook.json is empty. Add chunks before building the index.")
        return

    model = SentenceTransformer(str(MODEL_PATH))
    contents = [chunk["content"] for chunk in chunks]
    embeddings = model.encode(contents, show_progress_bar=True, convert_to_numpy=True)

    with open(INDEX_PATH, "wb") as f:
        pickle.dump({"embeddings": embeddings, "chunks": chunks}, f)

    print(f"Index built with {len(chunks)} chunks → saved to {INDEX_PATH}")


if __name__ == "__main__":
    build_index()
