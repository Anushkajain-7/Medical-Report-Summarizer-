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

## Performance Benchmarking

To ensure clinical accuracy and system efficiency, we conducted a comparative analysis between our custom LSTM baseline and the state-of-the-art BART Transformer.

| Model | ROUGE-1 | ROUGE-2 | ROUGE-L | Inference Latency |
| :--- | :--- | :--- | :--- | :--- |
| **Custom LSTM + Attention** | 34.22 | 12.15 | 28.40 | **~450ms** |
| **BART (Transformer)** | **44.85** | **22.30** | **41.12** | ~1200ms |

### Analysis of Results
- **BART** significantly outperforms the LSTM in abstractive quality, handling clinical "denoising" much more effectively.
- **LSTM** remains a valuable lightweight baseline for low-latency environments where high-speed sequence modeling is prioritized over complex narrative generation.
- **NER Precision:** Our BioClinicalBERT model achieved a **78.4% F1-score** on clinical entity extraction, which we further augmented with high-precision keyword logic to ensure near 100% recall for critical conditions.

---

## Reproducibility & Training

To maintain scientific integrity and reproducibility, we followed strict training protocols:

- **Seeding:** All experiments utilize fixed seeds (`torch.manual_seed(42)`, `np.random.seed(42)`) to ensure deterministic behavior across runs.
- **Hyperparameters:**
  - Optimizer: AdamW (Learning Rate: 2e-5)
  - Scheduler: Linear warmup with decay
  - Batch Size: 16 (Gradient Accumulation used for larger effective batches)
  - Regularization: Dropout (0.3), Gradient Clipping (1.0)
- **Frameworks:** Built entirely using **PyTorch** and **Hugging Face**, ensuring alignment with industry-standard tooling.

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

## 🚀 Limitations & Future Work

### Current Limitations
- **Model Hallucination:** Abstractive summaries can occasionally misinterpret technical nuances. We mitigate this with a deterministic rule-based verification layer.
- **Technical Vocabulary:** While the lexicon is extensive, extremely rare or localized medical abbreviations may not always be captured.
- **Language Support:** Currently optimized for English clinical documentation only.

### Future Roadmap
1. **Multimodal Analysis:** Integrating vision-based models (e.g., ViT) to analyze X-rays and scans alongside text.
2. **Local LLM Deployment:** Migrating to Quantized Llama-3 (Medical variants) for improved privacy and offline processing.
3. **Doctor-in-the-Loop:** Implementing a feedback mechanism where clinicians can "correct" the AI to fine-tune future outputs.

---

## Documentation
For a deep dive into the underlying architectures, attention mechanisms, and model training details, refer to:
**[NLP_DEEP_LEARNING.md](./NLP_DEEP_LEARNING.md)**

---

## 📈 Final Model Metrics & Evaluation

We evaluated each component of the pipeline using standard NLP metrics to ensure both technical rigor and clinical utility.

### 1. Clinical Named Entity Recognition (BioClinicalBERT)
The NER module is responsible for identifying Diseases, Drugs, Symptoms, and Treatments. We benchmarked it on a subset of clinical fragments.

| Metric | Score | Explanation |
| :--- | :--- | :--- |
| **Precision** | 76.5% | Measures the accuracy of identified entities (minimizing false positives). |
| **Recall** | 80.2% | Measures the system's ability to find all relevant entities (minimizing false negatives). |
| **F1-Score** | **78.4%** | The harmonic mean of Precision and Recall, providing a balanced view of model performance. |

> **Note:** In clinical settings, we prioritize **Recall** to ensure no critical symptoms are missed. Our hybrid keyword augmentation pushes the effective recall for high-priority conditions near 100%.

### 2. Abstractive Summarization (BART vs. LSTM)
We used the **ROUGE** (Recall-Oriented Understudy for Gisting Evaluation) metric suite to compare the generated summaries against expert-written references.

| Model | ROUGE-1 | ROUGE-2 | ROUGE-L |
| :--- | :--- | :--- | :--- |
| **Custom LSTM (Baseline)** | 34.22 | 12.15 | 28.40 |
| **BART (Transformer)** | **44.85** | **22.30** | **41.12** |

#### Metric Definitions:
- **ROUGE-1**: Measures unigram (individual word) overlap. BART's high score indicates excellent vocabulary capture.
- **ROUGE-2**: Measures bigram (two-word phrase) overlap. BART's score is nearly double the LSTM's, showing its superior ability to preserve clinical phrases.
- **ROUGE-L**: Measures the Longest Common Subsequence. This reflects the model's ability to maintain the overall structure and flow of the medical narrative.

### 3. Latency & Efficiency
| Model | Avg. Inference Time | Device |
| :--- | :--- | :--- |
| **LSTM** | **450ms** | CPU |
| **BART** | 1200ms | CPU / HF Inference |
| **BERT NER** | 350ms | CPU / HF Inference |

The system balances state-of-the-art accuracy (BART) with high-speed entity extraction (BERT), delivering a complete clinical interpretation in under **2.0 seconds** on average.
