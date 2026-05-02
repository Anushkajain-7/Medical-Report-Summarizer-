"""
Clinical Recommendation Layer
Provides deterministic, structured clinical guidance based on extracted medical entities.
"""

from typing import Dict, List, Any

# Medical Disclaimer - Must be attached to all outputs
MEDICAL_DISCLAIMER = (
    "DISCLAIMER: The following recommendations are generated automatically "
    "for informational purposes only. They do not constitute medical advice, "
    "diagnosis, or treatment. Always consult with a qualified healthcare "
    "professional before making any changes to your diet, lifestyle, or "
    "medication regimen."
)

# Knowledge Base: Maps disease entities (normalized) to structured recommendations
KNOWLEDGE_BASE = {
    "HYPERTENSION": {
        "recommended_actions": [
            "Monitor blood pressure daily at home.",
            "Take prescribed antihypertensive medications consistently.",
            "Engage in at least 150 minutes of moderate aerobic exercise per week."
        ],
        "things_to_avoid": [
            "Avoid skipping medication doses.",
            "Limit alcohol consumption.",
            "Avoid smoking and secondhand smoke."
        ],
        "diet_recommended": [
            "Adopt the DASH (Dietary Approaches to Stop Hypertension) diet.",
            "Increase intake of potassium-rich foods (e.g., bananas, spinach, sweet potatoes).",
            "Consume whole grains, lean proteins, and low-fat dairy."
        ],
        "diet_avoid": [
            "Strict sodium restriction (aim for < 1500mg per day).",
            "Avoid highly processed foods, canned soups, and fast food.",
            "Limit saturated fats and sugary beverages."
        ],
        "lifestyle": [
            "Manage stress through relaxation techniques or meditation.",
            "Maintain a healthy weight (BMI between 18.5 and 24.9).",
            "Ensure adequate sleep (7-8 hours per night)."
        ]
    },
    "TYPE 2 DIABETES MELLITUS": {
        "recommended_actions": [
            "Monitor blood glucose levels regularly as prescribed.",
            "Schedule regular HbA1c checks (typically every 3 months).",
            "Get annual comprehensive eye exams and daily foot checks.",
            "Take antidiabetic medications (e.g., Metformin) with meals to minimize GI upset."
        ],
        "things_to_avoid": [
            "Avoid prolonged periods of sedentary behavior.",
            "Do not walk barefoot to prevent unrecognized foot injuries."
        ],
        "diet_recommended": [
            "Focus on complex carbohydrates with a low glycemic index.",
            "Ensure a high intake of dietary fiber (vegetables, legumes).",
            "Portion control and consistent meal timing."
        ],
        "diet_avoid": [
            "Avoid refined carbohydrates and added sugars.",
            "Eliminate sugar-sweetened beverages and concentrated sweets.",
            "Limit saturated and trans fats."
        ],
        "lifestyle": [
            "Engage in a mix of aerobic and resistance training.",
            "Maintain meticulous foot hygiene."
        ]
    },
    "CONGESTIVE HEART FAILURE": {
        "recommended_actions": [
            "Weigh yourself daily every morning; report weight gain of >2 lbs/day or >5 lbs/week.",
            "Elevate legs to reduce edema.",
            "Take diuretics (e.g., Furosemide) exactly as prescribed."
        ],
        "things_to_avoid": [
            "Avoid NSAIDs (like Ibuprofen) as they can worsen fluid retention.",
            "Avoid intense physical exertion that causes severe shortness of breath."
        ],
        "diet_recommended": [
            "Fresh vegetables and fruits.",
            "Lean proteins."
        ],
        "diet_avoid": [
            "Strict sodium restriction (< 2000mg or as prescribed).",
            "Fluid restriction (e.g., < 1.5L to 2L per day) if advised by physician.",
            "Avoid salty snacks, cured meats, and canned foods."
        ],
        "lifestyle": [
            "Pace activities to conserve energy.",
            "Enroll in a cardiac rehabilitation program if recommended."
        ]
    },
    "BACTERIAL MENINGITIS": {
        "recommended_actions": [
            "Strict adherence to prescribed intravenous or oral antibiotics.",
            "Complete the entire course of medication even if symptoms improve.",
            "Rest in a quiet, dimly lit room to minimize photophobia and phonophobia.",
            "Monitor for neurological changes (confusion, worsening headache)."
        ],
        "things_to_avoid": [
            "Avoid bright lights and loud noises during acute recovery.",
            "Avoid strenuous physical activity until fully cleared by a physician."
        ],
        "diet_recommended": [
            "Maintain adequate hydration with clear fluids.",
            "Consume easily digestible, nutrient-dense foods during recovery."
        ],
        "diet_avoid": [
            "Avoid alcohol and potential neurotoxins.",
            "Avoid heavy, greasy foods if experiencing nausea."
        ],
        "lifestyle": [
            "Gradual return to normal activities.",
            "Follow-up for potential hearing or neurological assessments."
        ]
    },
    "UNSTABLE ANGINA": {
        "recommended_actions": [
            "Seek immediate emergency medical attention for prolonged or worsening chest pain.",
            "Take prescribed antiplatelet therapy (e.g., Aspirin, Clopidogrel) and statins.",
            "Keep Nitroglycerin accessible at all times."
        ],
        "things_to_avoid": [
            "Avoid strenuous exercise or heavy lifting until cleared by cardiology.",
            "Avoid cold exposure, which can trigger angina.",
            "Strict smoking cessation."
        ],
        "diet_recommended": [
            "Mediterranean diet approach.",
            "High intake of omega-3 fatty acids, fruits, and vegetables."
        ],
        "diet_avoid": [
            "Limit saturated fats, trans fats, and dietary cholesterol.",
            "Avoid large, heavy meals which divert blood flow to digestion."
        ],
        "lifestyle": [
            "Participate in closely monitored cardiac rehabilitation.",
            "Implement aggressive stress reduction techniques."
        ]
    }
}

# Aliases to map variations of disease names to our canonical keys
ALIASES = {
    "DIABETES": "TYPE 2 DIABETES MELLITUS",
    "TYPE 2 DIABETES": "TYPE 2 DIABETES MELLITUS",
    "T2DM": "TYPE 2 DIABETES MELLITUS",
    "HEART FAILURE": "CONGESTIVE HEART FAILURE",
    "CHF": "CONGESTIVE HEART FAILURE",
    "ANGINA": "UNSTABLE ANGINA",
    "MENINGITIS": "BACTERIAL MENINGITIS",
    "HIGH BLOOD PRESSURE": "HYPERTENSION"
}

def generate_recommendations(entities: Dict[str, List[str]]) -> Dict[str, Any]:
    """
    Generate structured clinical recommendations based on extracted disease entities.
    
    Args:
        entities: Dictionary containing extracted entities (e.g., {'DISEASE': ['Hypertension']})
        
    Returns:
        Dictionary mapping identified conditions to their recommendations, plus the medical disclaimer.
    """
    recommendations_output = {}
    
    # Only process diseases
    diseases = entities.get("DISEASE", [])
    
    for disease in diseases:
        normalized_disease = disease.upper().strip()
        
        # Check aliases
        if normalized_disease in ALIASES:
            normalized_disease = ALIASES[normalized_disease]
            
        # If we have a match in our knowledge base, add it
        if normalized_disease in KNOWLEDGE_BASE:
            recommendations_output[normalized_disease] = KNOWLEDGE_BASE[normalized_disease]
            
    # If no recognized diseases were found, return empty dict (handled by frontend)
    if not recommendations_output:
        return {"conditions": {}, "disclaimer": MEDICAL_DISCLAIMER}
        
    return {
        "conditions": recommendations_output,
        "disclaimer": MEDICAL_DISCLAIMER
    }
