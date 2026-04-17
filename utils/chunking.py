"""
Splits cleaned page text into chunks of 150-300 words.
Attaches metadata (chapter, section) to each chunk.
Saves output to data/textbook.json.
"""

import json
import re
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent.parent / "data" / "textbook.json"


def split_into_chunks(text: str, min_words: int = 150, max_words: int = 300) -> list[str]:
    """Splits text into chunks targeting max_words per chunk."""
    words = text.split()
    chunks = []
    current = []

    for word in words:
        current.append(word)
        if len(current) >= max_words:
            chunks.append(" ".join(current))
            current = []

    # Append remaining words if they meet minimum size
    if len(current) >= min_words:
        chunks.append(" ".join(current))
    elif chunks:
        # Merge small remainder into last chunk
        chunks[-1] += " " + " ".join(current)

    return chunks


def build_chunks(pages: list[str], chapter: str = "Unknown") -> list[dict]:
    full_text = "\n".join(pages)
    return split_by_headings(full_text, chapter)


def save_chunks(chunks: list[dict]):
    """Saves chunks to data/textbook.json."""
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(chunks)} chunks to {OUTPUT_PATH}")

def is_headline(line):
    if re.match(r'^\d+\.\d+\s+\w', line):
        return True
    words = line.strip().split()
    if len(words) >= 2 and len(words) <= 10 and sum(1 for w in words if w[0].isupper()) >= len(words) * 0.7:
        return True
    return False


def split_by_headings(text: str, chapter: str = "Unknown") -> list[dict]:
    chunks = []
    current_lines = []
    current_section = "Introduction"
    chunk_id = 1

    for line in text.split('\n'):
        stripped = line.strip()
        if not stripped:
            continue
        if is_headline(stripped):
            # save current accumulation if it has enough content
            content = " ".join(current_lines).strip()
            if len(content.split()) >= 50:
                chunks.append({
                    "id": chunk_id,
                    "chapter": chapter,
                    "section": current_section,
                    "content": content,
                })
                chunk_id += 1
            # start new section
            current_section = stripped
            current_lines = []
        else:
            current_lines.append(stripped)

    # save whatever is left after the loop
    content = " ".join(current_lines).strip()
    if len(content.split()) >= 50:
        chunks.append({
            "id": chunk_id,
            "chapter": chapter,
            "section": current_section,
            "content": content,
        })

    return chunks

