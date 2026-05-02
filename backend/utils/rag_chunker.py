"""
RAG-style Text Chunker
Splits long medical reports into overlapping chunks for better summarization.
"""

import re
from typing import List


def chunk_text(text: str, max_chunk_size: int = 1024, overlap: int = 128) -> List[str]:
    """
    Split text into overlapping chunks for RAG-style processing.
    Tries to split on sentence boundaries when possible.
    """
    if len(text) <= max_chunk_size:
        return [text]

    # Split into sentences first
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
            current_chunk += (" " + sentence if current_chunk else sentence)
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            # Start new chunk with overlap from previous
            if chunks and overlap > 0:
                prev = chunks[-1]
                overlap_text = prev[-overlap:] if len(prev) > overlap else prev
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk = sentence

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # Safeguard: Absolute limit on number of chunks to prevent OOM/DoS
    if len(chunks) > 20:
        chunks = chunks[:20]

    return chunks if chunks else [text[:max_chunk_size]]


def prepare_for_summarization(text: str, max_input_length: int = 3000) -> List[str]:
    """
    Prepare text chunks specifically for the summarization models.
    Ensures each chunk is within model input limits.
    """
    # Clean the text
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Safeguard: Truncate absolutely massive text blocks (e.g. 50,000 chars)
    if len(text) > 50000:
        text = text[:50000]

    return chunk_text(text, max_chunk_size=max_input_length, overlap=100)
