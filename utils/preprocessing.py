"""
Extracts and cleans text from a PDF file.
Uses PyMuPDF (fitz) for extraction.
"""

import re
import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> list[str]:
    """Returns a list of raw page texts from the PDF."""
    doc = fitz.open(pdf_path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return pages


def clean_text(text: str) -> str:
    """Removes common PDF noise: page numbers, figure captions, short noise labels."""
    # Remove standalone page numbers
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)
    # Remove figure captions (e.g. "FIGURE 1.1 ...")
    text = re.sub(r"^FIGURE\s+\d+\.\d+.*$", "", text, flags=re.MULTILINE)
    # Remove credit lines (e.g. "(Credit: ...)")
    text = re.sub(r"\s*\(Credit:[^)]*\)", "", text)
    # Remove short all-caps noise labels (e.g. "BRING IT HOME", "CHAPTER OBJECTIVES")
    text = re.sub(r"^[A-Z\s]{1,40}$", "", text, flags=re.MULTILINE)
    # Remove empty bullet points
    text = re.sub(r"^\s*•\s*$", "", text, flags=re.MULTILINE)
    # Remove end-of-chapter sections and everything after them
    for marker in ["Key Terms", "Key Concepts and Summary", "Self-Check Questions", "Review Questions", "Critical Thinking Questions", "Introduction to FRED"]:
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx]
    # Remove numbered review questions (e.g. "1. Why would..." or "21. Can you...")
    text = re.sub(r"^\d+\.\s+.+$", "", text, flags=re.MULTILINE)
    # Remove openstax footer
    text = re.sub(r"Access for free at openstax\.org.*$", "", text, flags=re.MULTILINE)
    # Remove bullet-prefixed footer lines (e.g. "1 • Critical Thinking Questions...")
    text = re.sub(r"^\d+\s*•.*$", "", text, flags=re.MULTILINE)
    # Collapse multiple blank lines into one
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Remove learning objectives
    text = re.sub(r"^By the end of this section.*$", "", text, flags=re.MULTILINE)
    text = text.strip()
    return text


def extract_and_clean(pdf_path: str) -> list[str]:
    """Full pipeline: extract → clean. Returns one cleaned string per page."""
    raw_pages = extract_text_from_pdf(pdf_path)
    return [clean_text(page) for page in raw_pages if clean_text(page)]
