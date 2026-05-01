"""
BART Summarizer Module
Uses facebook/bart-large-cnn via HuggingFace Inference API for abstractive summarization.
Falls back to a free summarization API if needed.
"""

import os
import requests
import time
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")
BART_API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"

# Persistent session for connection pooling (faster TCP/TLS handshakes)
session = requests.Session()
session.headers.update({"Authorization": f"Bearer {HF_API_TOKEN}"})


def _call_hf_api(text: str, max_length: int = 250, min_length: int = 50, retries: int = 3) -> Optional[str]:
    """Call HuggingFace Inference API for BART summarization."""
    payload = {
        "inputs": text[:1024],  # BART input limit
        "parameters": {
            "max_length": max_length,
            "min_length": min_length,
            "do_sample": False,
            "num_beams": 2, # Reduced from 4 for speed
            "early_stopping": True,
        },
        "options": {
            "wait_for_model": True,
            "use_cache": True,
        }
    }

    for attempt in range(retries):
        try:
            # Use persistent session instead of requests.post
            response = session.post(BART_API_URL, json=payload, timeout=90)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("summary_text", "")
                return ""
            elif response.status_code == 503:
                # Model is loading
                wait_time = response.json().get("estimated_time", 30)
                print(f"[BART] Model loading, waiting {wait_time}s (attempt {attempt+1}/{retries})")
                time.sleep(min(wait_time, 60))
            elif response.status_code == 429:
                print(f"[BART] Rate limited, waiting 10s (attempt {attempt+1}/{retries})")
                time.sleep(10)
            else:
                print(f"[BART] API error {response.status_code}: {response.text[:200]}")
                time.sleep(5)
        except requests.exceptions.Timeout:
            print(f"[BART] Request timeout (attempt {attempt+1}/{retries})")
            time.sleep(5)
        except Exception as e:
            print(f"[BART] Error: {e}")
            time.sleep(3)

    return None


def summarize_with_bart(text: str, max_length: int = 250, min_length: int = 50) -> dict:
    """
    Summarize text using BART-large-CNN via HuggingFace API.
    Returns dict with summary and metadata.
    """
    if not text or len(text.strip()) < 50:
        return {
            "summary": text,
            "model": "bart-large-cnn",
            "status": "text_too_short",
            "input_length": len(text),
        }

    summary = _call_hf_api(text, max_length=max_length, min_length=min_length)

    if summary is not None:
        return {
            "summary": summary,
            "model": "facebook/bart-large-cnn",
            "status": "success",
            "input_length": len(text),
            "output_length": len(summary),
        }

    # Fallback: extractive summarization
    sentences = text.replace('\n', ' ').split('. ')
    # Pick first 5 sentences as a basic extractive summary
    extractive = '. '.join(sentences[:5]) + '.'
    return {
        "summary": extractive,
        "model": "extractive-fallback",
        "status": "fallback",
        "input_length": len(text),
        "output_length": len(extractive),
    }


def summarize_chunks_with_bart(chunks: list, max_length: int = 200) -> dict:
    """
    Summarize multiple text chunks in parallel and combine results.
    Used for long documents that exceed BART's input limit.
    """
    if not chunks:
        return {"summary": "", "model": "none", "status": "no_chunks"}

    # Use ThreadPoolExecutor to run API calls in parallel
    # Limit workers to avoid being rate-limited by HF API
    max_workers = min(len(chunks), 4)
    summaries = [None] * len(chunks)

    def process_chunk(idx):
        result = summarize_with_bart(chunks[idx], max_length=max_length)
        return idx, result["summary"]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_chunk, range(len(chunks))))

    # Reassemble in order
    results.sort(key=lambda x: x[0])
    summaries = [r[1] for r in results]

    combined_summary = " ".join(summaries)
    print(f"[BART] {len(chunks)} chunks summarized in parallel")

    # If combined summary is still long, summarize again
    if len(combined_summary) > 1024 and len(chunks) > 1:
        final_result = summarize_with_bart(combined_summary, max_length=300)
        return {
            "summary": final_result["summary"],
            "model": final_result["model"],
            "status": "multi_pass",
            "chunks_processed": len(chunks),
        }

    return {
        "summary": combined_summary,
        "model": "facebook/bart-large-cnn",
        "status": "chunked",
        "chunks_processed": len(chunks),
    }
