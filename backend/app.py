"""
Medical Report Summarizer — FastAPI Backend
End-to-end pipeline: File Upload → Text Extraction → RAG Chunking →
BART Summarization → Clinical NER → ROUGE Evaluation

Endpoints:
  POST /analyze          — Upload file (PDF/DOCX/TXT) or raw text → full analysis
  POST /summarize        — Text-only summarization
  POST /ner              — Text-only NER extraction
  POST /rouge            — Compare two texts with ROUGE scores
  GET  /health           — Health check
  GET  /sample-reports   — Get sample medical reports for demo
"""

import os
import sys
import time
import asyncio

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.file_extractor import extract_text
from utils.rag_chunker import prepare_for_summarization
from pipeline.bart_summarizer import summarize_with_bart, summarize_chunks_with_bart
from pipeline.clinical_ner import extract_clinical_entities
from pipeline.rouge_eval import compute_rouge_scores, format_rouge_display

# ============================================================
# App Configuration
# ============================================================

app = FastAPI(
    title="Medical Report Summarizer API",
    description="End-to-end medical NLP pipeline with BART summarization and Clinical NER",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Request/Response Models
# ============================================================

class TextRequest(BaseModel):
    text: str
    max_length: Optional[int] = 250
    min_length: Optional[int] = 50


class RougeRequest(BaseModel):
    reference: str
    hypothesis: str


class AnalysisResponse(BaseModel):
    raw_text: str
    raw_text_snippet: str
    summary: str
    summary_model: str
    summary_status: str
    entities: dict
    rouge_scores: Optional[dict] = None
    processing_time: float
    input_length: int
    summary_length: int


# ============================================================
# Sample Medical Reports
# ============================================================

SAMPLE_REPORTS = [
    {
        "title": "Cardiology Consultation Report",
        "text": """CARDIOLOGY CONSULTATION REPORT

Patient: John Doe | Age: 67 | DOB: 03/15/1959
Date: 2024-01-15 | Referring Physician: Dr. Sarah Wilson

CHIEF COMPLAINT: Chest pain and shortness of breath on exertion for 3 weeks.

HISTORY OF PRESENT ILLNESS:
The patient is a 67-year-old male with a history of hypertension, type 2 diabetes mellitus, and hyperlipidemia who presents with progressive exertional chest pain and dyspnea over the past three weeks. The chest pain is described as substernal pressure, radiating to the left arm, occurring with moderate exertion such as climbing stairs. He rates the pain as 6/10 at its worst. The pain is relieved by rest within 5-10 minutes. He also reports associated symptoms of diaphoresis and mild nausea during episodes. He denies syncope, palpitations, or orthopnea. He has been compliant with his medications including metformin 1000mg twice daily, lisinopril 20mg daily, and atorvastatin 40mg daily.

PAST MEDICAL HISTORY:
1. Hypertension - diagnosed 2010, well-controlled on lisinopril
2. Type 2 Diabetes Mellitus - diagnosed 2012, HbA1c 7.2% (last checked 3 months ago)
3. Hyperlipidemia - on atorvastatin since 2015
4. Osteoarthritis - bilateral knees
5. Former smoker - quit 10 years ago, 20 pack-year history

MEDICATIONS:
1. Metformin 1000mg PO BID
2. Lisinopril 20mg PO daily
3. Atorvastatin 40mg PO at bedtime
4. Aspirin 81mg PO daily
5. Ibuprofen 400mg PRN for joint pain

PHYSICAL EXAMINATION:
Vitals: BP 148/92 mmHg, HR 78 bpm, RR 18, SpO2 96% on room air, Temp 98.4°F
General: Alert, oriented, mild distress with exertion
Cardiovascular: Regular rate and rhythm, S1 and S2 normal, no S3 or S4, no murmurs
Lungs: Clear to auscultation bilaterally, no wheezes or crackles
Extremities: No edema, peripheral pulses 2+ bilaterally

DIAGNOSTIC RESULTS:
ECG: Normal sinus rhythm, no ST-T wave changes at rest
Troponin I: 0.02 ng/mL (normal <0.04)
BNP: 125 pg/mL (mildly elevated)
Lipid Panel: Total cholesterol 210, LDL 130, HDL 42, Triglycerides 190
HbA1c: 7.2%
CBC: Within normal limits
BMP: Creatinine 1.1, eGFR 72

ASSESSMENT AND PLAN:
1. Unstable angina - Given progressive exertional symptoms with cardiac risk factors
   - Start clopidogrel 75mg daily
   - Schedule stress echocardiogram within 1 week
   - Consider cardiac catheterization if stress test positive
   - Continue aspirin 81mg daily

2. Hypertension - Suboptimally controlled (148/92)
   - Increase lisinopril to 40mg daily
   - Add amlodipine 5mg daily
   - Recheck BP in 2 weeks

3. Type 2 Diabetes - HbA1c at goal but borderline
   - Continue metformin 1000mg BID
   - Dietary counseling referral

4. Hyperlipidemia - LDL above target for high-risk patient
   - Increase atorvastatin to 80mg daily
   - Recheck lipid panel in 6 weeks

5. Discontinue ibuprofen due to cardiovascular risk; switch to acetaminophen for arthritis pain

FOLLOW-UP: Return in 2 weeks for BP check, sooner if symptoms worsen.

Dr. Michael Chen, MD, FACC
Board Certified Cardiologist"""
    },
    {
        "title": "Emergency Department Discharge Summary",
        "text": """EMERGENCY DEPARTMENT DISCHARGE SUMMARY

Patient: Jane Smith | Age: 45 | MRN: 2024-5678
Date: 2024-02-20 | ED Physician: Dr. Robert Kim

CHIEF COMPLAINT: Severe headache, fever, and neck stiffness for 24 hours.

HISTORY OF PRESENT ILLNESS:
45-year-old female presenting with acute onset severe headache rated 9/10, described as the "worst headache of her life," accompanied by fever (102.5°F at home), photophobia, phonophobia, neck stiffness, nausea, and vomiting. Symptoms began approximately 24 hours ago and have been progressively worsening. She denies recent trauma, travel, or sick contacts. She reports a recent upper respiratory infection 1 week ago that resolved. She has no history of migraines. She took acetaminophen 1000mg at home with minimal relief.

PAST MEDICAL HISTORY:
1. Asthma - mild intermittent, uses albuterol PRN
2. Depression - on sertraline 100mg daily
3. Seasonal allergies

MEDICATIONS:
1. Sertraline 100mg daily
2. Albuterol inhaler PRN
3. Cetirizine 10mg daily

PHYSICAL EXAMINATION:
Vitals: BP 135/85, HR 105, RR 20, Temp 102.8°F, SpO2 98%
General: Ill-appearing, photophobic, lying with eyes closed
HEENT: No papilledema on fundoscopy
Neck: Marked nuchal rigidity, positive Kernig sign, positive Brudzinski sign
Neuro: GCS 14 (E3V5M6), cranial nerves II-XII intact, no focal deficits
Skin: No petechiae or purpura

DIAGNOSTIC WORKUP:
CT Head without contrast: No acute intracranial pathology, no mass effect
Lumbar Puncture:
  - Opening pressure: 28 cmH2O (elevated)
  - WBC: 1,250/µL (95% neutrophils)
  - Protein: 180 mg/dL (elevated)
  - Glucose: 25 mg/dL (low, serum glucose 110)
  - Gram stain: Gram-positive diplococci
Blood Cultures: Sent, pending
CBC: WBC 18,500 with 90% neutrophils (left shift), Hgb 12.5, Plt 195
CRP: 185 mg/L (markedly elevated)
Procalcitonin: 8.5 ng/mL (elevated)

DIAGNOSIS: Bacterial Meningitis (likely Streptococcus pneumoniae based on Gram stain)

TREATMENT IN ED:
1. Ceftriaxone 2g IV initiated immediately after LP
2. Vancomycin 1g IV (empiric coverage pending cultures)
3. Dexamethasone 10mg IV (given before antibiotics)
4. IV Normal Saline 1L bolus for tachycardia
5. Ondansetron 4mg IV for nausea
6. Acetaminophen 1000mg IV for fever

DISPOSITION: Admitted to Medical ICU for close monitoring and continued IV antibiotics.

CONDITION ON TRANSFER: Stable but guarded. GCS improved to 15 after initial antibiotics and fluids.

Dr. Robert Kim, MD
Emergency Medicine"""
    },
    {
        "title": "Oncology Progress Note",
        "text": """ONCOLOGY PROGRESS NOTE

Patient: Maria Garcia | Age: 58 | MRN: 2024-9012
Date: 2024-03-10 | Oncologist: Dr. Jennifer Park

DIAGNOSIS: Stage IIIA Non-Small Cell Lung Cancer (Adenocarcinoma), diagnosed 2023-10-15

HISTORY:
58-year-old female with Stage IIIA NSCLC (adenocarcinoma), EGFR mutation negative, ALK negative, PD-L1 expression 60%. Initially presented with persistent cough, hemoptysis, and weight loss of 15 lbs over 3 months. Diagnosis confirmed by CT-guided biopsy of right upper lobe mass (4.5 cm) with mediastinal lymph node involvement. PET scan showed FDG uptake in primary tumor and ipsilateral mediastinal nodes (N2), no distant metastases.

TREATMENT HISTORY:
1. Completed 4 cycles of cisplatin/pemetrexed chemotherapy (Oct 2023 - Jan 2024)
2. Concurrent thoracic radiation therapy (60 Gy in 30 fractions, completed Feb 2024)
3. Currently on durvalumab (immunotherapy) consolidation - Cycle 3 of planned 12 months

CURRENT VISIT:
Patient reports improved energy levels compared to during chemoradiation. She notes mild fatigue 2-3 days after durvalumab infusion, which is manageable. Appetite has improved, gained 3 lbs since last visit. Denies new cough, hemoptysis, dyspnea, or chest pain. Reports mild intermittent nausea, controlled with ondansetron. She has occasional joint pain managed with acetaminophen. No skin rash or diarrhea (monitored for immune-related adverse events).

MEDICATIONS:
1. Durvalumab 10mg/kg IV every 2 weeks
2. Ondansetron 8mg PO PRN nausea
3. Acetaminophen 500mg PO PRN pain
4. Levothyroxine 50mcg daily (new - for durvalumab-induced hypothyroidism)
5. Omeprazole 20mg daily
6. Lorazepam 0.5mg PO PRN anxiety/insomnia

LABS:
CBC: WBC 5.2, Hgb 11.8 (improved from 10.2), Plt 210
CMP: All within normal limits, Creatinine 0.8
TSH: 6.8 (elevated, on levothyroxine - recheck in 4 weeks)
LFTs: AST 28, ALT 32, Alk Phos 85 (all normal)
CEA: 4.2 (down from 12.5 at diagnosis)

IMAGING:
CT Chest/Abdomen/Pelvis (2024-03-05):
- Right upper lobe mass: 2.1 cm (decreased from 4.5 cm at diagnosis, 3.0 cm post-chemoRT)
- Mediastinal lymph nodes: Decreased in size, largest 1.2 cm (previously 2.8 cm)
- No new lesions, no pleural effusion
- RECIST response: Partial Response (PR)

ASSESSMENT:
1. Stage IIIA NSCLC - Partial response to treatment, continuing to improve
2. Durvalumab-induced hypothyroidism - Being managed with levothyroxine
3. Treatment-related fatigue - Mild, improving

PLAN:
1. Continue durvalumab consolidation (Cycle 4 today)
2. Monitor thyroid function - recheck TSH in 4 weeks
3. Continue supportive medications
4. Next CT scan in 8 weeks
5. Monitor for immune-related adverse events
6. Nutritional counseling - continue weight gain efforts
7. Pneumococcal and influenza vaccination (timing per guidelines)

FOLLOW-UP: Return in 2 weeks for Cycle 5 durvalumab.

Dr. Jennifer Park, MD
Medical Oncology"""
    }
]


# ============================================================
# Warm-up Task (Background)
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Ping models on startup to warm them up."""
    print("[INIT] Warming up models...")
    # Fire and forget warm-up pings
    async def ping_models():
        try:
            # Short pings to trigger model loading
            from pipeline.bart_summarizer import _call_hf_api
            from pipeline.clinical_ner import _call_bert_ner
            
            # Just ping, don't wait for response in main thread
            asyncio.create_task(asyncio.to_thread(_call_hf_api, "Warmup", max_length=10, min_length=5))
            asyncio.create_task(asyncio.to_thread(_call_bert_ner, "Warmup"))
            print("[INIT] Warm-up pings sent to Hugging Face")
        except Exception as e:
            print(f"[INIT] Warm-up failed: {e}")
            
    asyncio.create_task(ping_models())

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Medical Report Summarizer",
        "version": "2.0.0",
        "models": {
            "summarizer": "facebook/bart-large-cnn",
            "ner": "dslim/bert-base-NER + clinical keywords",
            "lstm": "Seq2Seq with Bahdanau Attention",
        }
    }


@app.get("/sample-reports")
async def get_sample_reports():
    """Return sample medical reports for demonstration."""
    return {
        "reports": [
            {"title": r["title"], "text": r["text"]}
            for r in SAMPLE_REPORTS
        ]
    }


@app.post("/analyze")
async def analyze_report(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    max_length: int = Form(250),
    min_length: int = Form(50),
):
    """
    Full analysis pipeline:
    1. Extract text from file (PDF/DOCX/TXT) or use provided text
    2. Chunk text using RAG approach
    3. Summarize with BART
    4. Extract clinical entities with BERT NER + keywords
    5. Compute ROUGE scores (summary vs original)
    """
    start_time = time.time()

    # Get raw text
    raw_text = ""
    if file and file.filename:
        try:
            file_bytes = await file.read()
            raw_text = extract_text(file_bytes, file.filename)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"File extraction error: {str(e)}")
    elif text:
        raw_text = text.strip()
    else:
        raise HTTPException(status_code=400, detail="Provide either a file or text input.")

    if len(raw_text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Text is too short for meaningful analysis.")

    # Chunk for summarization (BART accepts ~1024 tokens ≈ 800 words ≈ 4000 chars)
    chunks = prepare_for_summarization(raw_text, max_input_length=3000)

    # Define sync wrappers for running in thread pool
    def run_summarize():
        if len(chunks) == 1:
            return summarize_with_bart(chunks[0], max_length=max_length, min_length=min_length)
        else:
            return summarize_chunks_with_bart(chunks, max_length=max_length)

    def run_raw_ner():
        return extract_clinical_entities(raw_text[:3000])

    # Run summarization AND raw-text NER simultaneously in thread pool
    summary_result, raw_entities = await asyncio.gather(
        asyncio.to_thread(run_summarize),
        asyncio.to_thread(run_raw_ner),
    )
    summary = summary_result["summary"]

    # Get entities from summary (after summary is ready)
    summary_entities = await asyncio.to_thread(extract_clinical_entities, summary)

    # Merge entities from raw text + summary for maximum coverage
    merged_entities = {}
    for category in ["DISEASE", "DRUG", "SYMPTOM", "TREATMENT"]:
        combined = set(raw_entities.get(category, []))
        combined.update(summary_entities.get(category, []))
        merged_entities[category] = sorted(list(combined))

    # ROUGE scores — use full raw_text (up to 5000 chars) for higher accuracy
    rouge = None
    try:
        rouge = await asyncio.to_thread(compute_rouge_scores, raw_text[:5000], summary)
    except Exception:
        pass

    processing_time = round(time.time() - start_time, 2)

    return {
        "raw_text": raw_text,
        "raw_text_snippet": raw_text[:500] + ("..." if len(raw_text) > 500 else ""),
        "summary": summary,
        "summary_model": summary_result.get("model", "unknown"),
        "summary_status": summary_result.get("status", "unknown"),
        "entities": merged_entities,
        "rouge_scores": rouge,
        "processing_time": processing_time,
        "input_length": len(raw_text),
        "summary_length": len(summary),
        "chunks_processed": len(chunks),
    }


@app.post("/summarize")
async def summarize_text(request: TextRequest):
    """Summarize text only (no NER)."""
    if len(request.text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Text too short.")

    chunks = prepare_for_summarization(request.text)
    if len(chunks) == 1:
        result = summarize_with_bart(chunks[0], request.max_length, request.min_length)
    else:
        result = summarize_chunks_with_bart(chunks, request.max_length)

    return result


@app.post("/ner")
async def extract_entities(request: TextRequest):
    """Extract clinical entities only."""
    if len(request.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Text too short.")

    entities = extract_clinical_entities(request.text)
    return {"entities": entities, "input_length": len(request.text)}


@app.post("/rouge")
async def compute_rouge(request: RougeRequest):
    """Compute ROUGE scores between two texts."""
    scores = compute_rouge_scores(request.reference, request.hypothesis)
    return {
        "scores": scores,
        "display": format_rouge_display(scores),
    }


# ============================================================
# Synthetic Document Test Endpoint
# ============================================================

SYNTHETIC_DOCS = [
    {
        "title": "Short Diabetes Management Note (No chunking)",
        "text": (
            "INTERNAL MEDICINE PROGRESS NOTE\n\n"
            "Patient: Robert Chen | Age: 52 | MRN: SYN-001\n"
            "Date: 2024-04-10 | Physician: Dr. Aisha Patel\n\n"
            "ASSESSMENT: Patient with Type 2 Diabetes Mellitus, poorly controlled (HbA1c 9.4%). "
            "Currently on Metformin 1000mg BID, but adherence is poor due to GI side effects. "
            "Presenting with fatigue, polyuria, and polydipsia for 2 weeks. "
            "Fasting glucose: 245 mg/dL. eGFR 78.\n\n"
            "PLAN: Increase Metformin to extended-release formulation to reduce GI symptoms. "
            "Add Sitagliptin 100mg daily. Dietary counseling referral. "
            "Diabetic eye exam and foot exam ordered. HbA1c recheck in 3 months.\n\n"
            "Dr. Aisha Patel, MD — Internal Medicine"
        )
    },
    {
        "title": "Long Multi-system Report (RAG chunking triggered)",
        "text": (
            "COMPREHENSIVE HOSPITAL DISCHARGE SUMMARY\n\n"
            "Patient: Sarah Nkosi | Age: 68 | MRN: SYN-002\n"
            "Admission: 2024-04-01 | Discharge: 2024-04-08 | Attending: Dr. James Okafor\n\n"
            "PRIMARY DIAGNOSIS: Acute decompensated congestive heart failure (CHF) with preserved ejection fraction.\n"
            "SECONDARY DIAGNOSES: Atrial fibrillation with rapid ventricular response, Type 2 Diabetes Mellitus, "
            "Chronic Kidney Disease Stage 3, Hypertension, Hyperlipidemia, Obesity (BMI 34.2).\n\n"
            "HISTORY OF PRESENT ILLNESS:\n"
            "68-year-old female with history of CHF-pEF, atrial fibrillation, and diabetes presented "
            "with 5-day history of progressively worsening dyspnea on exertion, bilateral leg swelling, "
            "orthopnea (requiring 3-pillow support), and a weight gain of 8 lbs over one week. "
            "She reports 2+ weeks of poor dietary compliance, consuming high-sodium foods. "
            "She denies chest pain, fever, or productive cough. Heart rate was 118 bpm on arrival, BP 168/94.\n\n"
            "HOSPITAL COURSE:\n"
            "Day 1-2: IV Furosemide 80mg BID initiated. Rate control with IV Metoprolol. "
            "Heparin infusion started for anticoagulation in setting of AF. O2 supplementation via nasal cannula. "
            "Cardiology consulted. Echocardiogram ordered.\n"
            "Day 3: Echocardiogram results — EF 55% (preserved), diastolic dysfunction Grade II, "
            "mild mitral regurgitation. Patient diuresed 3.2L net negative over 48 hours. "
            "Dyspnea significantly improved. Transitioned to oral Furosemide 40mg daily.\n"
            "Day 4-5: Oral Carvedilol 6.25mg BID initiated for rate control. Warfarin started "
            "for stroke prevention in AF (target INR 2-3). Lisinopril continued. Metformin held "
            "due to CKD — switched to Sitagliptin. HbA1c: 8.1%.\n"
            "Day 6-7: Patient ambulating independently. Weight normalized. Oxygen weaned off. "
            "Patient and family education on low-sodium diet, fluid restriction (1.5L/day), "
            "and daily weight monitoring. Cardiology recommends outpatient cardiac rehab.\n\n"
            "DISCHARGE MEDICATIONS:\n"
            "1. Furosemide 40mg PO daily\n2. Carvedilol 6.25mg PO BID\n3. Lisinopril 10mg PO daily\n"
            "4. Warfarin 5mg PO daily (INR goal 2-3)\n5. Atorvastatin 80mg PO at bedtime\n"
            "6. Sitagliptin 50mg PO daily (dose-reduced for CKD)\n7. Aspirin 81mg PO daily\n\n"
            "DISCHARGE INSTRUCTIONS: Daily weight monitoring — call if weight increases >2 lbs in one day "
            "or >5 lbs in one week. Low-sodium diet (<2g/day). Fluid restriction 1.5L/day. "
            "No NSAIDs. INR check in 3 days at clinic.\n\n"
            "FOLLOW-UP: Cardiology in 1 week. PCP in 2 weeks. Diabetes clinic in 1 month.\n\n"
            "Dr. James Okafor, MD — Hospitalist Medicine"
        )
    },
    {
        "title": "Very Long Oncology Trial Report (Heavy RAG test)",
        "text": (
            "ONCOLOGY CLINICAL TRIAL PROGRESS REPORT — TRIAL ID: SYNTH-TRIAL-2024\n\n"
            "Institution: Metro Cancer Center | Date: 2024-04-15\n"
            "Principal Investigator: Dr. Elena Rodriguez, MD, PhD\n"
            "Patient: Marcus Webb | Age: 61 | MRN: SYN-003\n\n"
            "PRIMARY DIAGNOSIS: Stage IV Metastatic Non-Small Cell Lung Cancer (NSCLC), "
            "Adenocarcinoma subtype. EGFR exon 19 deletion positive. PD-L1 TPS 30%.\n\n"
            "TRIAL BACKGROUND:\n"
            "This report covers Cycle 6 of a Phase II clinical trial evaluating the combination of "
            "Osimertinib (third-generation EGFR TKI) with Bevacizumab (anti-VEGF) versus Osimertinib "
            "monotherapy in EGFR-mutant advanced NSCLC. Patient enrolled 5 months ago after progression "
            "on first-generation Erlotinib therapy. Disease burden at enrollment: primary right lower lobe "
            "mass (5.8 cm), bilateral mediastinal lymphadenopathy, 3 liver metastases (largest 2.3 cm), "
            "right adrenal metastasis.\n\n"
            "TREATMENT HISTORY (PRE-TRIAL):\n"
            "1. Erlotinib 150mg daily — 14 months, then progression (T790M resistance mutation confirmed)\n"
            "2. Carboplatin + Pemetrexed x4 cycles — partial response, then progressive disease\n"
            "3. Enrolled in current trial — Osimertinib 80mg daily + Bevacizumab 15mg/kg q3 weeks\n\n"
            "CURRENT CYCLE (CYCLE 6) ASSESSMENT:\n"
            "Imaging — CT Chest/Abdomen/Pelvis (2024-04-12):\n"
            "- Primary mass: 2.9 cm (down from 5.8 cm at baseline — 50% reduction)\n"
            "- Mediastinal nodes: markedly decreased, largest now 0.8 cm\n"
            "- Liver metastases: 2 of 3 resolved; remaining lesion 0.7 cm\n"
            "- Adrenal metastasis: resolved\n"
            "- RECIST 1.1 Assessment: Partial Response (PR) maintained — 49.8% decrease in target lesions\n\n"
            "LABORATORY RESULTS:\n"
            "CBC: WBC 4.8 (normal), Hgb 10.9 (mild anemia), Plt 198 (normal)\n"
            "CMP: Creatinine 0.9, eGFR >90, LFTs all normal, Albumin 3.6\n"
            "CEA: 8.4 (down from 142 at baseline)\n"
            "ctDNA: EGFR exon 19 deletion variant allele frequency 0.8% (down from 18% at baseline)\n\n"
            "TREATMENT-RELATED ADVERSE EVENTS:\n"
            "- Diarrhea Grade 1: Managed with Loperamide PRN — resolved\n"
            "- Paronychia Grade 2: Treated with topical Betamethasone and oral Doxycycline — improving\n"
            "- Hypertension Grade 2 (Bevacizumab-related): BP 158/96 — added Amlodipine 5mg daily\n"
            "- Fatigue Grade 1: Persistent, managed with activity pacing and supportive care\n"
            "- No pneumonitis, no QTc prolongation, no hepatotoxicity\n\n"
            "PATIENT REPORTED OUTCOMES:\n"
            "Patient reports significantly improved quality of life compared to enrollment. "
            "Dyspnea has resolved, cough is minimal, and he has resumed light exercise. "
            "Appetite is good; weight stable. He denies hemoptysis, bone pain, or neurological symptoms. "
            "No new skin rash beyond existing paronychia. Sleep quality improved.\n\n"
            "BIOMARKER ANALYSIS:\n"
            "Serial liquid biopsy (ctDNA) demonstrates a 95.5% reduction in circulating tumor DNA, "
            "strongly correlating with radiographic response. This is consistent with deep molecular "
            "response to EGFR-directed therapy. No emergent resistance mutations (e.g., C797S, MET amplification) "
            "detected at this timepoint. Next NGS panel planned at Cycle 9 or at progression.\n\n"
            "PLAN FOR CYCLE 7:\n"
            "1. Continue Osimertinib 80mg PO daily (no dose modification needed)\n"
            "2. Bevacizumab 15mg/kg IV on Day 1 of Cycle 7 (in 3 weeks)\n"
            "3. Continue Amlodipine for hypertension management; recheck BP in 2 weeks\n"
            "4. Continue Doxycycline for paronychia; dermatology referral if no improvement\n"
            "5. Supportive care: Ondansetron PRN, Loperamide PRN, Vitamin B12 supplementation\n"
            "6. Repeat ctDNA at Cycle 9\n"
            "7. Next CT scan scheduled at Cycle 8 (approximately 6 weeks)\n"
            "8. Patient enrolled in quality-of-life sub-study — questionnaire completed\n"
            "9. Genetic counseling referral for family members given EGFR mutation status\n\n"
            "DISCUSSION:\n"
            "Patient is demonstrating an excellent response to the combination regimen. "
            "The sustained partial response at 6 cycles, combined with deep ctDNA reduction, "
            "suggests durable disease control. The primary concern going forward is monitoring "
            "for acquired resistance mechanisms and managing hypertension as a Bevacizumab-related "
            "class effect. Overall prognosis has improved significantly from initial staging.\n\n"
            "Dr. Elena Rodriguez, MD, PhD — Medical Oncology / Clinical Trials"
        )
    }
]


@app.get("/test-synthetic")
async def test_synthetic_docs():
    """
    Run the full pipeline on 3 synthetic documents of increasing complexity.
    Tests: RAG chunking, BART summarization, Clinical NER, and ROUGE scoring.
    Returns a structured report of results.
    """
    results = []

    for doc in SYNTHETIC_DOCS:
        start = time.time()
        text = doc["text"]
        chunks = prepare_for_summarization(text, max_input_length=3000)

        def run_summarize(chunks=chunks, text=text):
            if len(chunks) == 1:
                return summarize_with_bart(chunks[0], max_length=200, min_length=60)
            return summarize_chunks_with_bart(chunks, max_length=200)

        def run_ner(text=text):
            return extract_clinical_entities(text[:3000])

        summary_result, raw_entities = await asyncio.gather(
            asyncio.to_thread(run_summarize),
            asyncio.to_thread(run_ner),
        )

        rouge = None
        try:
            rouge = await asyncio.to_thread(compute_rouge_scores, text[:5000], summary_result["summary"])
        except Exception:
            pass

        results.append({
            "title":           doc["title"],
            "input_chars":     len(text),
            "chunks":          len(chunks),
            "summary":         summary_result["summary"],
            "summary_model":   summary_result.get("model", "unknown"),
            "summary_status":  summary_result.get("status", "unknown"),
            "entities":        raw_entities,
            "rouge_scores":    rouge,
            "processing_time": round(time.time() - start, 2),
        })

    return {"test_results": results, "total_docs": len(results)}


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
