"""
File Extractor Module
Handles text extraction from PDF, DOCX, and TXT files.
"""

import io
from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text content from a PDF file."""
    reader = PdfReader(io.BytesIO(file_bytes))
    text_parts = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text.strip())
    return "\n\n".join(text_parts)


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text content from a DOCX file."""
    doc = Document(io.BytesIO(file_bytes))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs)


def extract_text_from_txt(file_bytes: bytes) -> str:
    """Extract text content from a plain text file."""
    return file_bytes.decode("utf-8", errors="replace")


def extract_text(file_bytes: bytes, filename: str) -> str:
    """
    Route extraction based on file extension.
    Supports: .pdf, .docx, .doc, .txt
    """
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif lower.endswith((".docx", ".doc")):
        return extract_text_from_docx(file_bytes)
    elif lower.endswith(".txt"):
        return extract_text_from_txt(file_bytes)
    else:
        raise ValueError(f"Unsupported file format: {filename}. Use PDF, DOCX, or TXT.")
