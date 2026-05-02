"""
Clinical Intelligence Platform - FastAPI Backend
Intelligent medical report interpreter with proactive clinical pattern analysis.
"""

import os
import sys
import time
import asyncio

from dotenv import load_dotenv
load_dotenv()

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
from pipeline.clinical_recommendations import generate_intelligent_interpretation, MEDICAL_DISCLAIMER

app = FastAPI(
    title="Clinical Intelligence Assistant",
    description="Proactive medical report interpreter for patient empowerment.",
    version="4.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---

class AnalysisResponse(BaseModel):
    raw_text: str
    interpretation: Dict[str, Any]
    technical_summary: str
    findings: Dict[str, List[str]]
    meta: Dict[str, Any]

# --- Endpoints ---

@app.get("/health")
async def health_check():
    return {"status": "active", "intelligence_mode": "proactive_inference", "version": "4.0.0"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_report(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
):
    """
    Intelligent analysis pipeline with clinical pattern inference.
    """
    start_time = time.time()

    # 1. Ingest Text
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

    # 2. Extract Entities (BioClinicalBERT)
    # We do this first now because the inference engine depends on it
    def sync_ner():
        return extract_clinical_entities(raw_text[:4000]) # Scan more text for better context
    
    entities = await asyncio.to_thread(sync_ner)

    # 3. Clinical Inference & Interpretation
    # This layer analyzes the entities and text to find patterns (Infection, Cardiac, etc.)
    interpretation = await asyncio.to_thread(generate_intelligent_interpretation, entities, raw_text)

    # 4. Technical Summarization (BART)
    # We keep this as a secondary 'professional' summary
    chunks = prepare_for_summarization(raw_text, max_input_length=3000)
    def sync_sum():
        if len(chunks) == 1:
            return summarize_with_bart(chunks[0], max_length=300, min_length=100)
        return summarize_chunks_with_bart(chunks, max_length=300)

    summary_result = await asyncio.to_thread(sync_sum)
    technical_summary = summary_result["summary"]

    processing_time = round(time.time() - start_time, 2)

    return {
        "raw_text": raw_text,
        "interpretation": interpretation,
        "technical_summary": technical_summary,
        "findings": {
            "Medical Conditions": entities.get("DISEASE", []),
            "Medications": entities.get("DRUG", []),
            "Symptoms": entities.get("SYMPTOM", []),
            "Procedures & Tests": entities.get("TREATMENT", [])
        },
        "meta": {
            "processing_time": processing_time,
            "pattern_detected": interpretation["status_label"],
            "input_length": len(raw_text)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
