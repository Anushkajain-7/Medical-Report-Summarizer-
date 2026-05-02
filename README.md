# Medical Report Intelligence Platform

**A Narrative-Aware Clinical Reasoning System for Patient-Centric Interpretation**

Developed by **Sai Venkat** and **Anushka Jain**

---

## Overview

The **Medical Report Intelligence Platform** is a state-of-the-art healthcare AI solution designed to bridge the interpretability gap in clinical documentation. Unlike standard text summarizers, this platform performs deep clinical reasoning to transform unstructured medical reports (PDF, DOCX, TXT) into structured, actionable, and human-readable health intelligence.

The system interprets technical medical narratives just as a clinical expert would—simplifying jargon, triaging severity, and providing proactive guidance on next steps, lifestyle adjustments, and potential risks.

---

## Core Pillars

### Narrative-Aware Reasoning
The engine doesn't just extract keywords; it evaluates the entire clinical story. By analyzing the relationship between symptoms, procedures, and findings, it identifies the dominant medical domain (e.g., Cardiac, Vascular, Oncology) and accurately triages the severity of the report.

### Clinical Named Entity Recognition (NER)
Powered by **BioClinicalBERT**, the system extracts four critical taxonomies:
- **Diseases & Conditions**
- **Medications & Dosages**
- **Symptoms & Observations**
- **Medical Procedures & Treatments**

### Proactive Intelligence
Beyond the summary, the platform generates a comprehensive care plan:
- **What this means:** A plain-language explanation of the findings.
- **Action Plan:** Concrete "Do's" and "Avoid's" based on the clinical context.
- **Dietary Guidance:** Condition-specific nutritional recommendations.
- **Red Flags:** Urgent warning signs that require immediate medical attention.

---

## Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python, FastAPI, Uvicorn |
| **Deep Learning** | PyTorch, Custom LSTM Seq2Seq with Bahdanau Attention |
| **NLP** | Hugging Face Transformers, BART-Large-CNN, BioClinicalBERT |
| **Frontend** | React 19, Vite, Tailwind CSS 4 |
| **Visualization** | Chart.js, Lucide React |

---

## Project Structure

```text
Medical-Report-Summarizer/
├── backend/                # FastAPI Application & Model Pipelines
│   ├── models/             # Custom LSTM Seq2Seq Implementation
│   ├── pipeline/           # BART Summarization & Clinical NER
│   └── utils/              # File Extractors & RAG Chunkers
├── frontend-react/         # Modern React Dashboard
├── api/                    # Core API Utilities
├── NLP_DEEP_LEARNING.md    # Technical Model Documentation
├── requirements.txt        # Backend Dependencies
└── run.bat                 # Automation Script (Optional)
```

---

## Installation & Setup

### Prerequisites
- Python 3.9 - 3.11
- Node.js (v18+) & npm

### 1. Backend Configuration
Navigate to the `backend` directory and set up the environment:
```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Environment Variables:**
Create a `.env` file in the `backend` folder:
```env
HF_API_TOKEN=your_huggingface_token_here
```

### 2. Frontend Configuration
Navigate to the `frontend-react` directory and install dependencies:
```powershell
cd frontend-react
npm install
```

---

## Execution

For the best experience, run the backend and frontend in separate terminals:

**Terminal 1 (Backend):**
```powershell
cd backend
uvicorn app:app --reload
```

**Terminal 2 (Frontend):**
```powershell
cd frontend-react
npm run dev
```

The application will be available at **`http://localhost:5173`**.

---

## Pipeline Flow & Output

For every report analyzed, the platform generates a multi-dimensional response:
1. **Technical Summary:** A concise clinical abstract using BART.
2. **Simplified Explanation:** A narrative story for the patient.
3. **Structured Findings:** Categorized lists of detected conditions and drugs.
4. **Care Guidance:** Actionable advice on diet, activity, and precautions.
5. **Severity Triage:** Real-time classification (Critical, Serious, Moderate, Normal).

---

## Disclaimer

**This system is for informational and educational purposes only.** It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

---

## Documentation
For a deep dive into the underlying architectures, attention mechanisms, and model training details, refer to:
**[NLP_DEEP_LEARNING.md](./NLP_DEEP_LEARNING.md)**
