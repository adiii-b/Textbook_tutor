import re
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str) -> list[str]:
    reader = PdfReader(pdf_path)
    return [page.extract_text() or "" for page in reader.pages]


def clean_text(text: str) -> str:
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^FIGURE\s+\d+\.\d+.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s*\(Credit:[^)]*\)", "", text)
    text = re.sub(r"^[A-Z\s]{1,40}$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*•\s*$", "", text, flags=re.MULTILINE)
    for marker in ["Key Terms", "Key Concepts and Summary", "Self-Check Questions", "Review Questions", "Critical Thinking Questions", "Introduction to FRED"]:
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx]
    text = re.sub(r"^\d+\.\s+.+$", "", text, flags=re.MULTILINE)
    text = re.sub(r"Access for free at openstax\.org.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\d+\s*•.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"^By the end of this section.*$", "", text, flags=re.MULTILINE)
    return text.strip()


def extract_and_clean(pdf_path: str) -> list[str]:
    raw_pages = extract_text_from_pdf(pdf_path)
    return [clean_text(page) for page in raw_pages if clean_text(page)]
