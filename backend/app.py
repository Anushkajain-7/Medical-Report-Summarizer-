"""
Clinical Intelligence Platform - FastAPI Backend
Intelligent medical report interpreter with narrative-aware clinical reasoning.
"""

import os
import sys
import time
import asyncio
import requests

from dotenv import load_dotenv
# Explicitly find .env in the current directory (backend/)
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Any, Dict

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.file_extractor import extract_text
from utils.rag_chunker import prepare_for_summarization
from pipeline.bart_summarizer import summarize_with_bart, summarize_chunks_with_bart
from pipeline.clinical_ner import extract_clinical_entities
from pipeline.clinical_recommendations import generate_proactive_intelligence, MEDICAL_DISCLAIMER

app = FastAPI(
    title="Clinical Reasoning Assistant",
    description="Advanced narrative-aware medical report interpreter.",
    version="5.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- State ---
api_token_valid = None

@app.on_event("startup")
async def startup_event():
    """Verify HF_API_TOKEN on startup."""
    global api_token_valid
    token = os.getenv("HF_API_TOKEN", "").strip()
    
    if not token or "PASTE" in token:
        api_token_valid = False
        return

    try:
        res = requests.get(
            "https://huggingface.co/api/whoami-v2",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        api_token_valid = (res.status_code == 200)
    except Exception:
        api_token_valid = None

# --- Models ---

class AnalysisResponse(BaseModel):
    raw_text: str
    technical_summary: str
    clinical_intelligence: Dict[str, Any]
    findings: Dict[str, List[str]]
    meta: Dict[str, Any]

# --- Endpoints ---

@app.get("/health")
async def health_check():
    return {
        "status": "active", 
        "engine_version": "5.0.0",
        "api_token_status": "valid" if api_token_valid else "invalid" if api_token_valid == False else "unknown"
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_report(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
):
    """
    Multi-stage clinical reasoning pipeline.
    """
    start_time = time.time()

    # 1. Ingest
    raw_text = ""
    if file and file.filename:
        try:
            file_bytes = await file.read()
            raw_text = extract_text(file_bytes, file.filename)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"File extraction failed: {str(e)}")
    elif text:
        raw_text = text.strip()
    else:
        raise HTTPException(status_code=400, detail="Please provide a medical report to analyze.")

    if len(raw_text) < 20:
        raise HTTPException(status_code=400, detail="Document content is too brief for analysis.")

    # 2. Extract Entities (Stage 1)
    def sync_ner():
        return extract_clinical_entities(raw_text[:4000])
    
    entities = await asyncio.to_thread(sync_ner)

    # 3. Clinical Reasoning (Stage 2-5)
    # This engine handles domain, severity, and priority overrides
    intelligence = await asyncio.to_thread(generate_proactive_intelligence, entities, raw_text)

    # 4. Professional Summarization
    chunks = prepare_for_summarization(raw_text, max_input_length=3000)
    def sync_sum():
        if len(chunks) == 1:
            return summarize_with_bart(chunks[0], max_length=350, min_length=150)
        return summarize_chunks_with_bart(chunks, max_length=350)

    summary_result = await asyncio.to_thread(sync_sum)
    technical_summary = summary_result["summary"]

    processing_time = round(time.time() - start_time, 2)

    return {
        "raw_text": raw_text,
        "technical_summary": technical_summary,
        "clinical_intelligence": intelligence,
        "findings": {
            "Medical Conditions": entities.get("DISEASE", []),
            "Medications": entities.get("DRUG", []),
            "Symptoms": entities.get("SYMPTOM", []),
            "Procedures & Tests": entities.get("TREATMENT", [])
        },
        "meta": {
            "processing_time": processing_time,
            "engine": "Clinical Intelligence v5.0",
            "domain": intelligence["main_concern"],
            "severity": intelligence["severity_level"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
