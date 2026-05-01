"""
Clinical NER Module
Uses BERT-based NER (dslim/bert-base-NER) via HuggingFace API +
comprehensive keyword-based clinical entity extraction.
Extracts: DISEASE, DRUG, SYMPTOM, TREATMENT entities.
"""

import os
import re
import requests
import time
from typing import Dict, List, Optional
from collections import defaultdict

HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")
NER_API_URL = "https://router.huggingface.co/hf-inference/models/dslim/bert-base-NER"

# Persistent session for connection pooling
session = requests.Session()
session.headers.update({"Authorization": f"Bearer {HF_API_TOKEN}"})

# ============================================================
# Comprehensive Medical Keyword Dictionaries
# ============================================================

DISEASE_KEYWORDS = [
    "diabetes", "hypertension", "cancer", "tumor", "carcinoma", "lymphoma", "leukemia",
    "melanoma", "sarcoma", "adenoma", "glioma", "meningioma", "pneumonia", "bronchitis",
    "asthma", "copd", "emphysema", "tuberculosis", "hepatitis", "cirrhosis",
    "alzheimer", "parkinson", "epilepsy", "multiple sclerosis", "stroke", "aneurysm",
    "atherosclerosis", "coronary artery disease", "heart failure", "arrhythmia",
    "atrial fibrillation", "myocardial infarction", "heart attack",
    "arthritis", "osteoarthritis", "rheumatoid arthritis", "lupus", "fibromyalgia",
    "osteoporosis", "gout", "anemia", "sickle cell", "hemophilia", "thrombosis",
    "embolism", "deep vein thrombosis", "pulmonary embolism",
    "kidney disease", "renal failure", "nephritis", "urinary tract infection",
    "appendicitis", "cholecystitis", "pancreatitis", "colitis", "crohn",
    "celiac disease", "gastritis", "ulcer", "gerd", "irritable bowel",
    "infection", "sepsis", "meningitis", "encephalitis", "endocarditis",
    "hiv", "aids", "covid", "influenza", "malaria", "dengue",
    "thyroid", "hypothyroidism", "hyperthyroidism", "cushing",
    "obesity", "metabolic syndrome", "hyperlipidemia", "hypercholesterolemia",
    "depression", "anxiety", "schizophrenia", "bipolar disorder", "ptsd",
    "dementia", "delirium", "neuropathy", "radiculopathy", "stenosis",
    "fracture", "dislocation", "concussion", "contusion", "laceration",
    "edema", "inflammation", "fibrosis", "necrosis", "ischemia", "infarction",
    "abscess", "cyst", "polyp", "nodule", "lesion", "mass", "growth",
    "dysfunction", "insufficiency", "deficiency", "disorder", "syndrome",
    "disease", "condition", "pathology", "malignancy", "neoplasm",
    "type 2 diabetes", "type 1 diabetes", "gestational diabetes",
    "chronic kidney disease", "acute kidney injury", "congestive heart failure",
]

DRUG_KEYWORDS = [
    "metformin", "insulin", "glipizide", "glyburide", "sitagliptin",
    "lisinopril", "enalapril", "ramipril", "losartan", "valsartan",
    "amlodipine", "nifedipine", "diltiazem", "verapamil",
    "atenolol", "metoprolol", "propranolol", "carvedilol", "bisoprolol",
    "hydrochlorothiazide", "furosemide", "spironolactone", "chlorthalidone",
    "aspirin", "clopidogrel", "warfarin", "heparin", "enoxaparin", "rivaroxaban",
    "atorvastatin", "rosuvastatin", "simvastatin", "pravastatin",
    "omeprazole", "pantoprazole", "esomeprazole", "ranitidine", "famotidine",
    "amoxicillin", "azithromycin", "ciprofloxacin", "levofloxacin", "doxycycline",
    "cephalexin", "ceftriaxone", "vancomycin", "metronidazole", "clindamycin",
    "prednisone", "prednisolone", "dexamethasone", "hydrocortisone", "methylprednisolone",
    "ibuprofen", "naproxen", "acetaminophen", "paracetamol", "tylenol",
    "morphine", "oxycodone", "hydrocodone", "fentanyl", "tramadol", "codeine",
    "gabapentin", "pregabalin", "duloxetine", "amitriptyline",
    "sertraline", "fluoxetine", "escitalopram", "citalopram", "paroxetine",
    "venlafaxine", "bupropion", "mirtazapine", "trazodone",
    "lorazepam", "diazepam", "alprazolam", "clonazepam", "midazolam",
    "quetiapine", "risperidone", "olanzapine", "aripiprazole", "haloperidol",
    "levothyroxine", "methimazole", "propylthiouracil",
    "albuterol", "fluticasone", "budesonide", "montelukast", "ipratropium",
    "nitroglycerin", "digoxin", "amiodarone", "dobutamine", "dopamine",
    "epinephrine", "norepinephrine", "vasopressin",
    "ondansetron", "metoclopramide", "promethazine",
    "mg", "mcg", "units", "tablet", "capsule", "injection", "infusion",
    "medication", "drug", "prescription", "dose", "dosage",
]

SYMPTOM_KEYWORDS = [
    "pain", "headache", "migraine", "chest pain", "abdominal pain", "back pain",
    "joint pain", "muscle pain", "neck pain", "pelvic pain",
    "fever", "chills", "sweating", "night sweats", "malaise",
    "fatigue", "weakness", "lethargy", "drowsiness", "insomnia",
    "nausea", "vomiting", "diarrhea", "constipation", "bloating",
    "cough", "shortness of breath", "dyspnea", "wheezing", "stridor",
    "tachycardia", "bradycardia", "palpitations", "chest tightness",
    "dizziness", "vertigo", "syncope", "lightheadedness", "confusion",
    "numbness", "tingling", "tremor", "seizure", "paralysis",
    "swelling", "rash", "itching", "bruising", "bleeding", "discharge",
    "weight loss", "weight gain", "appetite loss", "anorexia",
    "difficulty breathing", "difficulty swallowing", "dysphagia",
    "urinary frequency", "urinary urgency", "hematuria", "dysuria",
    "blurred vision", "double vision", "hearing loss", "tinnitus",
    "anxiety", "agitation", "irritability", "mood changes",
    "tenderness", "stiffness", "cramping", "spasm", "rigidity",
    "jaundice", "cyanosis", "pallor", "diaphoresis", "edema",
    "hemoptysis", "epistaxis", "melena", "hematochezia",
    "dyspepsia", "heartburn", "flatulence", "distension",
    "sore throat", "hoarseness", "congestion", "rhinorrhea",
    "photophobia", "phonophobia", "aura",
]

TREATMENT_KEYWORDS = [
    "surgery", "operation", "procedure", "biopsy", "resection", "excision",
    "transplant", "implant", "graft", "bypass", "angioplasty", "stent",
    "chemotherapy", "radiation", "radiotherapy", "immunotherapy",
    "dialysis", "transfusion", "intubation", "ventilation", "ventilator",
    "catheter", "catheterization", "drainage", "debridement",
    "physical therapy", "occupational therapy", "speech therapy",
    "rehabilitation", "therapy", "counseling", "psychotherapy",
    "cast", "splint", "brace", "prosthesis", "orthosis",
    "suture", "staple", "wound care", "dressing change",
    "monitoring", "observation", "follow-up", "referral", "consultation",
    "screening", "vaccination", "immunization", "prophylaxis",
    "diet", "lifestyle modification", "exercise program",
    "oxygen therapy", "nebulizer", "inhaler", "cpap", "bipap",
    "iv fluids", "parenteral nutrition", "enteral feeding",
    "epidural", "nerve block", "local anesthesia", "general anesthesia",
    "ecg", "ekg", "echocardiogram", "ultrasound", "mri", "ct scan",
    "x-ray", "mammogram", "colonoscopy", "endoscopy", "bronchoscopy",
    "blood test", "urinalysis", "culture", "sensitivity",
    "treatment", "intervention", "management", "regimen", "protocol",
    "admission", "discharge", "transfer", "icu", "intensive care",
]


def _call_bert_ner(text: str) -> Optional[List[dict]]:
    """Call HuggingFace BERT NER API."""
    payload = {
        "inputs": text[:512],
        "options": {"wait_for_model": True, "use_cache": True}
    }

    try:
        # Use persistent session
        response = session.post(NER_API_URL, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 503:
            wait = response.json().get("estimated_time", 20)
            print(f"[NER] Model loading, waiting {wait}s...")
            time.sleep(min(wait, 45))
            response = session.post(NER_API_URL, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json()
        print(f"[NER] API error {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"[NER] Error: {e}")

    return None


def _map_ner_label(label: str) -> Optional[str]:
    """Map standard NER labels to clinical categories."""
    label = label.upper().replace("B-", "").replace("I-", "")
    mapping = {
        "MISC": "DISEASE",
        "ORG": "TREATMENT",
        "PER": None,
        "LOC": None,
        "DISEASE": "DISEASE",
        "DRUG": "DRUG",
        "SYMPTOM": "SYMPTOM",
        "TREATMENT": "TREATMENT",
    }
    return mapping.get(label)


def _keyword_extraction(text: str) -> Dict[str, List[str]]:
    """Extract clinical entities using keyword matching."""
    text_lower = text.lower()
    entities = defaultdict(set)

    # Pre-compile regex for performance if not already done
    # (In a production app, these would be global)
    for category, keywords in [
        ("DISEASE", DISEASE_KEYWORDS),
        ("DRUG", DRUG_KEYWORDS),
        ("SYMPTOM", SYMPTOM_KEYWORDS),
        ("TREATMENT", TREATMENT_KEYWORDS)
    ]:
        # Sort keywords by length descending to match longer phrases first
        sorted_keywords = sorted(keywords, key=len, reverse=True)
        pattern = re.compile(r'\b(' + '|'.join(map(re.escape, sorted_keywords)) + r')\b', re.IGNORECASE)
        
        matches = pattern.findall(text)
        for match in matches:
            if len(match) >= 2:
                entities[category].add(match.strip())

    # Case-insensitive deduplication: keep the capitalized version
    deduped = {}
    for k, v in entities.items():
        seen = {}
        for item in v:
            lower = item.lower()
            if lower not in seen or item[0].isupper():
                seen[lower] = item
        deduped[k] = sorted(seen.values(), key=str.lower)
    return deduped


def extract_clinical_entities(text: str) -> Dict[str, List[str]]:
    """
    Extract clinical entities (DISEASE, DRUG, SYMPTOM, TREATMENT) from text.
    Uses BERT NER + comprehensive keyword extraction.
    """
    entities = defaultdict(set)

    # 1. Try BERT NER API
    ner_results = _call_bert_ner(text)
    if ner_results and isinstance(ner_results, list):
        for entity in ner_results:
            if isinstance(entity, dict):
                word = entity.get("word", "")
                # Skip BERT sub-word tokens (##...) and reconstruct grouped entities
                if word.startswith("##"):
                    continue
                word = word.replace("##", "").strip()
                label = entity.get("entity_group", entity.get("entity", ""))
                clinical_label = _map_ner_label(label)
                # Only add real words: min 3 chars, score threshold, no truncated artefacts
                score = entity.get("score", 1.0)
                # Filter: min 3 chars, confidence >= 0.7, looks like a real word/phrase
                is_real_word = re.match(r"^[A-Za-z][A-Za-z\s\-']{2,}$", word) is not None
                # Verify it actually appears as a whole word in the text (avoids sub-word fragments)
                appears_whole = bool(re.search(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE))
                if clinical_label and len(word) >= 3 and score >= 0.7 and is_real_word and appears_whole:
                    entities[clinical_label].add(word)

    # 2. Keyword-based extraction (always runs as augmentation)
    keyword_entities = _keyword_extraction(text)
    for category, items in keyword_entities.items():
        entities[category].update(items)

    # 3. Convert to sorted lists — filter any remaining artefacts
    def clean_entities(items):
        cleaned = set()
        for item in items:
            item = item.strip()
            # Must be at least 3 chars, no lone numbers, no single-char suffix artefacts
            if len(item) >= 3 and not item.isnumeric():
                cleaned.add(item)
        return sorted(cleaned, key=str.lower)

    result = {
        "DISEASE":   clean_entities(entities.get("DISEASE", set())),
        "DRUG":      clean_entities(entities.get("DRUG", set())),
        "SYMPTOM":   clean_entities(entities.get("SYMPTOM", set())),
        "TREATMENT": clean_entities(entities.get("TREATMENT", set())),
    }

    return result
