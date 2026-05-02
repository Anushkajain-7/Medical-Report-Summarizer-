"""
Clinical Inference & Intelligence Layer
Analyzes clinical patterns and provides proactive, patient-centric interpretation.
"""

from typing import Dict, List, Any, Set

# Medical Disclaimer - Mandatory
MEDICAL_DISCLAIMER = (
    "DISCLAIMER: This analysis is provided by an AI clinical assistant for educational purposes. "
    "It is NOT a medical diagnosis or a replacement for a doctor's evaluation. "
    "If you are feeling unwell, seek professional medical help immediately."
)

# 1. Pattern Definitions (Keywords/Entities that suggest a clinical concern)
CLINICAL_PATTERNS = {
    "INFECTION_INFLAMMATION": {
        "keywords": ["WBC", "FEVER", "CRP", "PROCALCITONIN", "NEUTROPHILS", "INFECTION", "SEPSIS", "BACTERIAL", "VIRAL", "COUGH", "NAUSEA", "VOMITING", "CHILLS"],
        "drugs": ["CEFTRIAXONE", "VANCOMYCIN", "AMOXICILLIN", "AZITHROMYCIN", "CIPROFLOXACIN", "ANTIBIOTIC"],
        "label": "Infection or Inflammation",
        "explanation": "The report suggests signs of an immune response, likely due to an infection or inflammation in the body. This is often indicated by elevated white blood counts (WBC) or markers like CRP.",
        "red_flags": ["High fever over 103°F", "Confusion or disorientation", "Severe shivering", "Difficulty breathing"],
        "guidance": {
            "do": ["Stay hydrated with water and electrolytes.", "Get plenty of restorative rest.", "Complete any prescribed antibiotic courses exactly as directed."],
            "avoid": ["Avoid intense physical activity.", "Limit contact with others if a contagious infection is suspected.", "Avoid alcohol while on medication."],
            "diet": ["Clear soups and broths.", "Stay hydrated with clear fluids.", "Easily digestible foods like crackers or toast."],
            "diet_avoid": ["Heavy, greasy foods.", "Spicy foods if experiencing nausea.", "Highly processed snacks."],
            "lifestyle": ["Monitor your temperature every 4-6 hours.", "Practice good hand hygiene.", "Ensure a quiet, comfortable recovery environment."]
        }
    },
    "CARDIAC_CONCERN": {
        "keywords": ["CHEST PAIN", "DYSPNEA", "SHORTNESS OF BREATH", "BNP", "TROPONIN", "BP", "BLOOD PRESSURE", "HYPERTENSION", "ANGINA", "HEART", "MURMUR", "PALPITATIONS", "EDEMA", "SWELLING"],
        "drugs": ["LISINOPRIL", "AMLODIPINE", "ATORVASTATIN", "ASPIRIN", "NITROGLYCERIN", "FUROSEMIDE", "METOPROLOL", "CARVEDILOL"],
        "label": "Cardiovascular Function",
        "explanation": "The report indicates findings related to your heart or blood pressure. This could include markers of heart strain (like BNP/Troponin) or signs of fluid buildup and high blood pressure.",
        "red_flags": ["Severe chest pressure or squeezing", "Pain spreading to the arm or jaw", "Sudden difficulty breathing while resting", "Sudden fainting or severe dizziness"],
        "guidance": {
            "do": ["Monitor your blood pressure and heart rate daily.", "Keep a record of any chest pain episodes.", "Take prescribed heart medications consistently."],
            "avoid": ["Avoid heavy lifting or sudden intense strain.", "Limit salt (sodium) intake immediately.", "Avoid smoking and secondhand smoke."],
            "diet": ["Leafy greens, fish, and nuts.", "Fresh fruits and vegetables.", "Whole grains (oats, brown rice)."],
            "diet_avoid": ["Strictly limit salt (sodium) to less than 2,000mg per day.", "Avoid fried foods and trans fats.", "Limit red meat and high-fat dairy."],
            "lifestyle": ["Engage in light, physician-cleared walking.", "Manage stress through deep breathing.", "Weigh yourself daily to monitor for sudden fluid buildup."]
        }
    },
    "METABOLIC_SUGAR": {
        "keywords": ["GLUCOSE", "HBA1C", "DIABETES", "SUGAR", "HYPERGLYCEMIA", "METABOLIC", "INSULIN", "POLYURIA", "THIRST", "FATIGUE"],
        "drugs": ["METFORMIN", "SITAGLIPTIN", "INSULIN", "GLIPIZIDE", "EMPAGLIFLOZIN"],
        "label": "Blood Sugar & Metabolism",
        "explanation": "The findings suggest concerns with how your body processes sugar. High levels of glucose or HbA1c indicate that your blood sugar may be consistently above the ideal range.",
        "red_flags": ["Extreme thirst and frequent urination", "Fruity-smelling breath", "Sudden blurred vision", "Extreme weakness or confusion"],
        "guidance": {
            "do": ["Monitor your blood sugar levels as recommended.", "Keep a log of your carbohydrate intake.", "Check your feet daily for any small cuts or sores."],
            "avoid": ["Avoid skipping meals, which can cause sugar crashes.", "Avoid sugary snacks and sodas.", "Limit high-starch foods (potatoes, white bread)."],
            "diet": ["High-fiber vegetables (broccoli, leafy greens).", "Lean proteins (chicken, fish, tofu).", "Lentils and beans."],
            "diet_avoid": ["Avoid refined sugars and syrups.", "Limit white rice and pasta.", "Avoid fruit juices and energy drinks."],
            "lifestyle": ["Engage in 20-30 minutes of light activity after meals.", "Ensure consistent sleep patterns.", "Stay hydrated with plain water."]
        }
    },
    "ANEMIA_BLOOD_CONCERN": {
        "keywords": ["HEMOGLOBIN", "HGB", "ANEMIA", "FATIGUE", "PALLOR", "IRON", "B12", "FERRITIN", "BRUISING"],
        "drugs": ["IRON SUPPLEMENT", "VITAMIN B12", "FOLATE", "EPOETIN"],
        "label": "Blood Count & Oxygen",
        "explanation": "The report shows findings related to your red blood cells or hemoglobin levels. This may suggest that your body is struggling to carry enough oxygen to your tissues, often causing fatigue.",
        "red_flags": ["Severe shortness of breath with minimal effort", "Rapid or irregular heartbeat", "Severe dizziness or fainting", "Extreme, unexplained fatigue"],
        "guidance": {
            "do": ["Take prescribed iron or vitamin supplements.", "Combine iron-rich foods with Vitamin C for better absorption.", "Schedule a follow-up blood test to track progress."],
            "avoid": ["Avoid drinking tea or coffee immediately after meals (as they block iron absorption).", "Avoid intense exercise until your levels improve."],
            "diet": ["Lean red meat or fortified cereals.", "Spinach, kale, and legumes.", "Citrus fruits (to help absorb iron)."],
            "diet_avoid": ["Limit processed snacks with zero nutritional value.", "Avoid excessive caffeine.", "Limit calcium supplements at the same time as iron-rich meals."],
            "lifestyle": ["Pace your daily activities to conserve energy.", "Get up slowly from sitting or lying down to avoid dizziness.", "Ensure adequate rest."]
        }
    },
    "RESPIRATORY_CONCERN": {
        "keywords": ["COUGH", "DYSPNEA", "SHORTNESS OF BREATH", "SPO2", "OXYGEN", "LUNG", "ASTHMA", "PNEUMONIA", "WHEEZING", "HEMOPTYSIS"],
        "drugs": ["ALBUTEROL", "SYMBICORT", "PREDNISONE", "DEXAMETHASONE", "SPIRIVA"],
        "label": "Respiratory & Lung Health",
        "explanation": "The findings suggest concerns with your breathing or lung function. This could be due to temporary inflammation, chronic conditions like asthma, or acute issues like pneumonia.",
        "red_flags": ["Struggling to catch your breath while resting", "Bluish tint to lips or fingernails", "Chest pain when breathing deeply", "Severe, persistent coughing"],
        "guidance": {
            "do": ["Use prescribed inhalers as directed.", "Practice pursed-lip breathing if you feel short of breath.", "Monitor your oxygen levels (SpO2) if a device is available."],
            "avoid": ["Strictly avoid smoking and vaping.", "Avoid strong perfumes, smoke, or other lung irritants.", "Avoid very cold, dry air if it triggers coughing."],
            "diet": ["Stay well-hydrated to help thin mucus.", "Small, frequent meals if large meals make it harder to breathe."],
            "diet_avoid": ["Limit dairy if it increases mucus production for you.", "Avoid heavy, salt-rich foods that cause bloating."],
            "lifestyle": ["Ensure your living area is free from dust and allergens.", "Keep your head elevated while sleeping.", "Engage in light, steady activity as tolerated."]
        }
    },
    "PAIN_INJURY_TRAUMA": {
        "keywords": ["PAIN", "FRACTURE", "TRAUMA", "SWELLING", "EDEMA", "INJURY", "OSTEOARTHRITIS", "JOINT", "BONE", "LIMPING"],
        "drugs": ["IBUPROFEN", "ACETAMINOPHEN", "NAPROXEN", "MORPHINE", "GABAPENTIN"],
        "label": "Pain, Injury, or Bone Health",
        "explanation": "The report discusses pain, injury, or concerns with your bones and joints. This may range from temporary muscle strain to more significant issues like fractures or chronic joint wear.",
        "red_flags": ["Sudden, severe swelling in one limb", "Inability to bear weight on a limb", "Pain that is not relieved by rest or medication", "Numbness or tingling below an injury site"],
        "guidance": {
            "do": ["Follow the R.I.C.E. protocol (Rest, Ice, Compression, Elevation) for new injuries.", "Take pain relief medication as directed by your doctor.", "Use supports like braces or crutches if provided."],
            "avoid": ["Avoid putting weight on an injured area until cleared.", "Avoid movements that increase sharp pain.", "Avoid 'pushing through' severe pain."],
            "diet": ["Calcium-rich foods (yogurt, cheese, leafy greens) for bone health.", "Foods rich in Vitamin D.", "Anti-inflammatory foods like ginger or turmeric."],
            "diet_avoid": ["Limit inflammatory foods like refined sugars.", "Avoid excessive alcohol, which can slow healing."],
            "lifestyle": ["Alternate rest with gentle range-of-motion exercises if cleared.", "Apply heat or cold packs as recommended for your specific pain.", "Ensure your footwear provides proper support."]
        }
    },
    "WELLNESS_NORMAL": {
        "label": "General Wellness & Monitoring",
        "explanation": "Your report appears to show mostly stable or expected findings. Most markers checked are within or near the typical range for someone of your profile.",
        "red_flags": ["New or worsening pain", "Unexplained weight loss", "Persistent fatigue that does not improve with rest", "Any sudden change in your usual health baseline"],
        "guidance": {
            "do": ["Continue your current healthy routines.", "Schedule your next routine check-up.", "Keep a simple log of how you feel day-to-day."],
            "avoid": ["Avoid making major changes to your health routine without consulting a professional.", "Avoid excessive stress or overexertion."],
            "diet": ["Maintain a balanced diet of whole foods.", "Stay hydrated with 8 glasses of water daily.", "Focus on a variety of colorful vegetables."],
            "diet_avoid": ["Limit processed and fast foods.", "Avoid excessive sugar and salt.", "Limit saturated fats."],
            "lifestyle": ["Aim for 150 minutes of moderate activity per week.", "Prioritize 7-9 hours of quality sleep.", "Practice daily stress-relief techniques like walking or reading."]
        }
    }
}

def infer_clinical_pattern(entities: Dict[str, List[str]], raw_text: str) -> Dict[str, Any]:
    """
    Analyzes extracted entities and raw text to infer the most likely clinical concern.
    """
    detected_patterns = []
    
    # Collect all evidence
    all_evidence = set()
    for cat in entities.values():
        for item in cat:
            all_evidence.add(item.upper().strip())
    
    # Check each pattern
    for pid, pdata in CLINICAL_PATTERNS.items():
        if pid == "WELLNESS_NORMAL": continue
        
        score = 0
        # Check keywords
        for kw in pdata.get("keywords", []):
            if kw in all_evidence or kw in raw_text.upper():
                score += 1
        
        # Check drugs
        for drug in pdata.get("drugs", []):
            if drug in all_evidence or drug in raw_text.upper():
                score += 2 # Drugs are stronger indicators
                
        if score >= 2:
            detected_patterns.append((pid, score))
            
    # Sort by score and pick top
    detected_patterns.sort(key=lambda x: x[1], reverse=True)
    
    # If no pattern detected, return Wellness
    if not detected_patterns:
        return CLINICAL_PATTERNS["WELLNESS_NORMAL"]
    
    # Merge top patterns (if scores are close)
    primary_pid = detected_patterns[0][0]
    return CLINICAL_PATTERNS[primary_pid]

def generate_intelligent_interpretation(entities: Dict[str, List[str]], raw_text: str) -> Dict[str, Any]:
    """
    Generates a human-readable interpretation and Care Plan based on clinical inference.
    """
    pattern = infer_clinical_pattern(entities, raw_text)
    
    # Construct Interpretation
    interpretation = {
        "status_label": pattern["label"],
        "simple_explanation": pattern["explanation"],
        "red_flags": pattern["red_flags"],
        "care_plan": {
            "do": pattern["guidance"]["do"],
            "avoid": pattern["guidance"]["avoid"],
            "diet_recommended": pattern["guidance"]["diet"],
            "diet_restricted": pattern["guidance"]["diet_avoid"],
            "lifestyle": pattern["guidance"]["lifestyle"]
        },
        "disclaimer": MEDICAL_DISCLAIMER
    }
    
    return interpretation
