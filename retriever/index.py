import json
import pickle
from pathlib import Path
from retriever.embedder import encode_corpus

DATA_PATH = Path(__file__).parent.parent / "data" / "textbook.json"
INDEX_PATH = Path(__file__).parent.parent / "data" / "bm25_index.pkl"


def build_index():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    if not chunks:
        print("textbook.json is empty. Add chunks before building the index.")
        return

    contents = [chunk["content"] for chunk in chunks]
    embeddings = encode_corpus(contents)

    with open(INDEX_PATH, "wb") as f:
        pickle.dump({"embeddings": embeddings, "chunks": chunks}, f)

    print(f"Index built with {len(chunks)} chunks → saved to {INDEX_PATH}")


if __name__ == "__main__":
    build_index()
