"""
Clinical Intelligence & Reasoning Engine (v5.0)
Advanced multi-stage reasoning for patient-centric medical report interpretation.
"""

from typing import Dict, List, Any, Optional, Set
import re

# --- Constants & Disclaimers ---
MEDICAL_DISCLAIMER = (
    "DISCLAIMER: This analysis is provided by an AI health assistant for educational purposes only. "
    "It is NOT a medical diagnosis, clinical opinion, or replacement for professional care. "
    "In case of emergency, call your local emergency services (e.g., 911) or visit the nearest ER immediately."
)

# --- 1. Clinical Domains & Narrative Markers ---
# We use a scoring system to determine the "Dominant Domain"
DOMAINS = {
    "VASCULAR_EMERGENCY": {
        "label": "Critical Vascular Event",
        "priority": 100, # Highest priority
        "critical_markers": ["RUPTURE", "HEMORRHAGE", "ANEURYSM", "DISSECTION", "INTERNAL BLEEDING", "EMERGENCY SURGERY", "VASCULAR CONSULT", "FATAL", "EXPIRATION", "DEATH"],
        "narrative_cues": ["PROGRESSED TO RUPTURE", "IDENTIFIED POST-MORTEM", "SURGICAL INTERVENTION REQUIRED", "ACUTE ONSET"],
        "severity": "CRITICAL"
    },
    "CARDIAC": {
        "label": "Cardiovascular Condition",
        "priority": 80,
        "critical_markers": ["MYOCARDIAL INFARCTION", "HEART ATTACK", "UNSTABLE ANGINA", "CARDIAC ARREST", "SHOCK"],
        "keywords": ["CHEST PAIN", "BNP", "TROPONIN", "ECG", "EKG", "STENOSIS", "ISCHEMIA", "CHF", "HEART FAILURE"],
        "severity_map": {"SHOCK": "CRITICAL", "INFARCTION": "SERIOUS", "ANGINA": "SERIOUS", "CHF": "MODERATE"}
    },
    "INFECTION_SEPSIS": {
        "label": "Infectious Disease / Sepsis",
        "priority": 70,
        "critical_markers": ["SEPSIS", "SEPTIC SHOCK", "MENINGITIS", "BACTEREMIA"],
        "keywords": ["WBC", "FEVER", "CRP", "PROCALCITONIN", "NEUTROPHILS", "PNEUMONIA", "ABSCESS"],
        "severity_map": {"SHOCK": "CRITICAL", "SEPSIS": "SERIOUS", "MENINGITIS": "SERIOUS"}
    },
    "TRAUMA_SURGICAL": {
        "label": "Acute Trauma or Surgical Event",
        "priority": 75,
        "critical_markers": ["TRAUMA", "FRACTURE", "HEMORRHAGE", "LACERATION", "POST-OPERATIVE COMPLICATION"],
        "keywords": ["PAIN", "SWELLING", "SURGERY", "PROCEDURE", "INTUBATION"],
        "severity_map": {"HEMORRHAGE": "CRITICAL", "FRACTURE": "MODERATE"}
    },
    "NEUROLOGICAL": {
        "label": "Neurological Event",
        "priority": 85,
        "critical_markers": ["STROKE", "CVA", "ANEURYSM", "HEMORRHAGE", "SEIZURE", "GCS"],
        "keywords": ["CONFUSION", "HEADACHE", "STIFFNESS", "NEURO", "SYNCOPE"],
        "severity_map": {"STROKE": "CRITICAL", "HEMORRHAGE": "CRITICAL", "SEIZURE": "SERIOUS"}
    },
    "METABOLIC_ENDOCRINE": {
        "label": "Metabolic or Endocrine Concern",
        "priority": 50,
        "critical_markers": ["KETOACIDOSIS", "DKA", "HYPOGLYCEMIA"],
        "keywords": ["GLUCOSE", "HBA1C", "DIABETES", "THYROID", "METFORMIN"],
        "severity_map": {"KETOACIDOSIS": "SERIOUS", "HYPOGLYCEMIA": "SERIOUS"}
    },
    "ONCOLOGY": {
        "label": "Oncological Findings",
        "priority": 65,
        "critical_markers": ["METASTASIS", "MALIGNANT", "CARCINOMA"],
        "keywords": ["TUMOR", "MASS", "LESION", "BIOPSY", "CHEMOTHERAPY", "STAGE"],
        "severity_map": {"METASTASIS": "SERIOUS", "MALIGNANT": "SERIOUS"}
    }
}

# --- 2. Guidance Engine (Domain-Aware) ---
GUIDANCE_DATABASE = {
    "CRITICAL": {
        "explanation": "The report indicates an extremely serious medical event requiring immediate specialized intervention. It discusses life-threatening complications or urgent surgical needs.",
        "do": ["Ensure immediate follow-up with the primary surgical or clinical team.", "Verify all medication changes with a specialist.", "Maintain strict monitoring in a clinical setting."],
        "avoid": ["Do not delay emergency medical care.", "Avoid any strenuous activity.", "Do not ignore new or worsening pain."],
        "diet": ["Strict adherence to NPO (nothing by mouth) if surgery is pending.", "Follow specific hospital-directed nutrition plan."],
        "red_flags": ["Sudden worsening of symptoms", "New onset of severe pain", "Loss of consciousness", "Severe bleeding"]
    },
    "SERIOUS": {
        "explanation": "This report highlights significant clinical findings that require active medical management and close monitoring to prevent complications.",
        "do": ["Adhere strictly to prescribed medication schedules.", "Schedule urgent follow-up with your specialist.", "Monitor vital signs as directed."],
        "avoid": ["Avoid heavy physical strain.", "Do not skip follow-up appointments.", "Avoid self-medicating with over-the-counter drugs."],
        "diet": ["Adopt a condition-specific diet (e.g., Low Sodium, DASH, or Diabetic).", "Ensure adequate hydration unless restricted."],
        "red_flags": ["Worsening shortness of breath", "Chest pain", "High fever that does not break", "Sudden confusion"]
    },
    "MODERATE": {
        "explanation": "The report describes a stable but important medical condition that requires ongoing care and lifestyle adjustments.",
        "do": ["Keep a daily log of symptoms or labs.", "Review findings with your doctor during the next visit.", "Maintain regular light activity as tolerated."],
        "avoid": ["Avoid known triggers for your condition.", "Limit habits that worsen your symptoms (e.g., smoking, high salt)."],
        "diet": ["Focus on a balanced whole-food diet.", "Monitor portion sizes and nutritional labels."],
        "red_flags": ["New symptoms that interfere with daily life", "Persistent pain", "Unexplained fatigue"]
    },
    "NORMAL_WELLNESS": {
        "explanation": "The report shows mostly routine or stable findings that do not indicate an acute medical crisis at this time.",
        "do": ["Continue routine health screenings.", "Maintain regular exercise.", "Ensure your vaccinations are up to date."],
        "avoid": ["Avoid excessive stress or poor sleep.", "Limit processed foods."],
        "diet": ["Maintain a colorful, balanced diet.", "Drink 8 glasses of water daily."],
        "red_flags": ["Any sudden deviation from your usual health baseline"]
    }
}

# --- 3. Reasoning Pipeline ---

class ClinicalReasoner:
    def __init__(self, entities: Dict[str, List[str]], raw_text: str):
        self.entities = entities
        self.raw_text = raw_text.upper()
        self.domain = "GENERAL_MEDICAL"
        self.severity = "MODERATE"
        self.findings = []
        self.interpretation = ""

    def _detect_story_pattern(self) -> Dict[str, Any]:
        """Stage 2: Classify domain and severity based on the whole narrative."""
        scores = {k: 0 for k in DOMAINS.keys()}
        
        # Check for critical overrides first
        for domain_id, data in DOMAINS.items():
            # Narrative cues are weighted heavily
            for cue in data.get("narrative_cues", []):
                if cue in self.raw_text:
                    scores[domain_id] += 50
            
            # Critical markers are weighted
            for marker in data.get("critical_markers", []):
                if marker in self.raw_text or any(marker in e.upper() for e in self.entities.get("DISEASE", [])):
                    scores[domain_id] += 30
                    self.findings.append(marker)
            
            # General keywords
            for kw in data.get("keywords", []):
                if kw in self.raw_text:
                    scores[domain_id] += 5

        # Determine dominant domain
        sorted_domains = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_domain_id, top_score = sorted_domains[0]
        
        if top_score < 10:
            return {"domain_id": "GENERAL_MEDICAL", "severity": "MODERATE", "label": "General Medical Monitoring"}
        
        # Determine Severity based on domain and markers
        domain_data = DOMAINS[top_domain_id]
        severity = domain_data.get("severity", "MODERATE")
        
        # Check severity map within the domain
        for marker, sev in domain_data.get("severity_map", {}).items():
            if marker in self.raw_text:
                severity = sev # Escalates severity

        return {
            "domain_id": top_domain_id,
            "severity": severity,
            "label": domain_data["label"]
        }

    def _generate_explanation(self, domain_info: Dict[str, Any]) -> str:
        """Stage 3: Generate a contextual plain-language story."""
        label = domain_info["label"]
        severity = domain_info["severity"]
        
        if severity == "CRITICAL":
            return (
                f"This report describes a critical {label.lower()} event. "
                "The findings indicate a major medical emergency, such as a rupture or severe complication, "
                "that required urgent specialist intervention. The focus of the report is on life-saving measures "
                "and acute hospital management."
            )
        elif severity == "SERIOUS":
            return (
                f"The report highlights a serious {label.lower()} concern. "
                "There are significant findings, such as acute inflammation or cardiac strain, "
                "that require active medical treatment and careful monitoring by your healthcare team."
            )
        else:
            return (
                f"This report appears to focus on {label.lower()}. "
                "It describes important findings that need to be managed, but they do not appear "
                "to represent an immediate medical crisis based on the provided text."
            )

    def analyze(self) -> Dict[str, Any]:
        """Execute the full reasoning pipeline."""
        # 1. Classify the 'Story'
        domain_info = self._detect_story_pattern()
        self.domain = domain_info["domain_id"]
        self.severity = domain_info["severity"]
        
        # 2. Generate Explanation
        self.interpretation = self._generate_explanation(domain_info)
        
        # 3. Fetch Guidance
        guidance = GUIDANCE_DATABASE.get(self.severity, GUIDANCE_DATABASE["MODERATE"])
        
        # 4. Construct Final Output
        return {
            "main_concern": domain_info["label"],
            "severity_level": self.severity,
            "what_this_means": self.interpretation,
            "key_highlights": sorted(list(set(self.findings))),
            "care_plan": {
                "do": guidance["do"],
                "avoid": guidance["avoid"],
                "diet": guidance["diet"],
                "red_flags": guidance["red_flags"]
            },
            "disclaimer": MEDICAL_DISCLAIMER
        }

def generate_proactive_intelligence(entities: Dict[str, List[str]], raw_text: str) -> Dict[str, Any]:
    """External entry point for the Clinical Reasoning Engine."""
    reasoner = ClinicalReasoner(entities, raw_text)
    return reasoner.analyze()
