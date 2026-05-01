# Medical Report Summarizer with Clinical NER

> End-to-end medical NLP pipeline with LSTM Seq2Seq summarization and BERT clinical NER.

## Quick Start

### 1. Start the Backend

```bash
cd backend
source venv/bin/activate
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Start the Frontend

```bash
cd frontend
python3 -m http.server 5173
```

### 3. Open in Browser

Navigate to **http://localhost:5173**

---

## 📂 Project Structure

```
Medical-report-summerizer/
├── backend/
│   ├── app.py                          # FastAPI main application
│   ├── .env                            # HuggingFace API token
│   ├── requirements.txt                # Python dependencies
│   ├── models/
│   │   └── lstm_seq2seq.py             # LSTM Seq2Seq + Bahdanau Attention
│   ├── pipeline/
│   │   ├── bart_summarizer.py          # BART summarization (HuggingFace API)
│   │   ├── clinical_ner.py             # BERT NER + keyword extraction
│   │   └── rouge_eval.py              # ROUGE metric computation
│   ├── train/
│   │   └── train_lstm.py              # LSTM training script (CNN/DailyMail)
│   └── utils/
│       ├── file_extractor.py          # PDF/DOCX/TXT extraction
│       └── rag_chunker.py            # RAG text chunking
└── frontend/
    ├── index.html                     # Main HTML
    ├── style.css                      # Premium dark theme CSS
    └── app.js                         # Frontend JavaScript
```

## Pipeline Architecture

```
Upload (PDF/DOCX/TXT) → Extract Text → RAG Chunk → BART Summarize → BERT NER → ROUGE Evaluate
```

### DL Objective — LSTM Seq2Seq
- 2-layer stacked bidirectional LSTM encoder (hidden=512)
- Bahdanau (additive) attention mechanism
- Decoder with teacher forcing (ratio=0.5)
- Adam optimizer + gradient clipping (max_norm=1.0)
- Packed sequences for variable lengths
- Trained on CNN/DailyMail dataset
- ROUGE-L target: 0.41
- Ablation: attention vs no-attention

### NLP Objective — Transformers + Clinical NER
- **BART**: facebook/bart-large-cnn via HuggingFace Inference API
- **BERT NER**: dslim/bert-base-NER for entity extraction
- **Entities**: DISEASE, DRUG, SYMPTOM, TREATMENT
- **Pipeline**: Summarize → Extract entities from summary
- **Output**: Raw report | Summary | Extracted entities side-by-side

## Key Technologies
- **PyTorch** — LSTM Seq2Seq model
- **HuggingFace** — BART, BERT NER via Inference API
- **FastAPI** — REST API backend
- **ROUGE** — Evaluation metrics (ROUGE-1, ROUGE-2, ROUGE-L)
- **PyPDF2 / python-docx** — File extraction
- **RAG** — Sentence-boundary-aware text chunking

## Training the LSTM

```bash
cd backend
source venv/bin/activate
python train/train_lstm.py --epochs 5 --batch_size 16 --max_samples 5000 --ablation
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/sample-reports` | GET | Get sample medical reports |
| `/analyze` | POST | Full pipeline (file/text → summary + NER + ROUGE) |
| `/summarize` | POST | Text-only summarization |
| `/ner` | POST | Text-only entity extraction |
| `/rouge` | POST | Compare two texts with ROUGE |
