# Medical Report Summarizer and Clinical NER Pipeline

## Project Overview

The Medical Report Summarizer is an end-to-end natural language processing (NLP) pipeline designed to process raw, unstructured clinical text and medical reports. The system ingests documentation in various formats (PDF, DOCX, TXT) and orchestrates a multi-stage process to extract actionable insights. It generates highly concise, abstractive summaries using both custom Long Short-Term Memory (LSTM) sequence models and state-of-the-art transformer-based architectures (BART). Concurrently, the pipeline executes clinical Named Entity Recognition (NER) utilizing a fine-tuned BioClinicalBERT model to structure critical medical data into distinct taxonomies, including diseases, drugs, symptoms, and medical treatments. 

This project addresses a critical real-world problem in the healthcare sector: information overload. Clinical documentation often consists of dense, unstructured text that is highly inefficient for medical professionals to parse manually during time-sensitive diagnostic processes. By automating the extraction of core findings and structured entities, this pipeline aims to reduce cognitive load on physicians, streamline medical record auditing, and provide the foundational infrastructure for advanced clinical decision support systems.

## Motivation and Academic Objectives

The architecture of this repository was heavily influenced by the necessity to bridge foundational deep learning theories with modern applied machine learning paradigms. Academically, the project fulfills the stringent requirements of advanced Deep Learning and Natural Language Processing coursework (e.g., CSR311, CSR322). It serves as a comprehensive demonstration of sequence modeling by implementing a custom two-layer stacked bidirectional LSTM encoder-decoder architecture augmented with Bahdanau attention mechanisms. 

Practically, the pipeline transitions from theoretical sequence models to industry-standard transformer architectures by integrating pre-trained and fine-tuned variants of Facebook's BART. This dual-model approach allows for rigorous empirical ablation studies and performance benchmarking. The integration of the NER module further demonstrates the capacity to utilize domain-specific masked language models (BioClinicalBERT) for targeted entity extraction, proving highly applicable to contemporary healthcare analytics and automated report processing workloads.

## System Architecture

The pipeline operates on a robust, modular architecture governed by a FastAPI backend backend orchestrator and an asynchronous React frontend. When a raw document is ingested, it undergoes text extraction and normalization. Because transformer models possess strict token context limits, the text is subsequently processed by a Retrieval-Augmented Generation (RAG)-inspired chunking module. This component intelligently segments lengthy medical histories into overlapping chunks to preserve semantic continuity across token boundaries.

Following segmentation, the text is routed through two parallel computational streams. The summarization stream passes the segmented data to the summarization engine, which dynamically routes the request to either the transformer-based BART model or the custom attention-guided LSTM network. Simultaneously, the NER stream processes the text using a BioClinicalBERT model, executing token classification to identify and categorize medical terminology. The outputs from these independent streams are aggregated by the backend orchestrator. Finally, an integrated evaluation module mathematically scores the generated abstractive summaries against reference ground truths using the ROUGE metric suite. This consolidated data payload is then serialized and transmitted to the React frontend, where it is rendered via a sophisticated analytical dashboard.

## Getting Started

### 1. Backend Setup and Configuration

The backend is engineered with FastAPI and relies heavily on PyTorch and the Hugging Face ecosystem. It is recommended to deploy this within an isolated Python virtual environment.

```bash
cd Medical-Report-Summarizer--main/backend
python -m venv venv
```

**On Windows (PowerShell):**
```powershell
venv\Scripts\activate
pip install -r requirements.txt
```

**On Unix/MacOS (Bash):**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

The transformer inference models require authentication via the Hugging Face API. You must create a `.env` file in the `backend` directory and supply your API token.

```bash
# backend/.env
HF_API_TOKEN=your_huggingface_access_token
```

### 2. Model Training and Benchmarking

The repository provides automated scripts for both fine-tuning the transformer models and training the custom LSTM architecture from scratch.

To execute the LSTM training script with the built-in attention ablation study:
```bash
python backend/train/train_lstm.py --epochs 5 --batch_size 16 --ablation
```

To execute the BART fine-tuning sequence on the target dataset:
```bash
python backend/train/train_bart.py --epochs 3 --batch_size 4
```

To run the unified performance benchmark comparing latency and ROUGE metrics across all models:
```bash
python backend/benchmark.py
```

### 3. Launching the Application Services

The project is designed for rapid local deployment. Once the backend environment is configured and the Hugging Face token is set, you can launch both the backend and frontend simultaneously using a single command.

#### **Option A: Unified Launch (Recommended for Windows)**
From the root directory, execute the batch script:
```bash
run.bat
```
*This will automatically instantiate the FastAPI backend (Port 8000) and the Vite development server (Port 5173) in separate terminal windows.*

#### **Option B: Manual Launch (Step-by-Step)**

**1. Instantiate the Backend Server:**
The application utilizes Uvicorn as the ASGI web server implementation.
```bash
cd backend
venv\Scripts\activate
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**2. Initialize the Frontend Interface:**
In a separate terminal session, start the React development server.
```bash
cd frontend-react
npm install
npm run dev
```

The platform will be accessible at `http://localhost:5173`. The frontend automatically handles the proxy routing to the backend API at `http://localhost:8000`.

## Project Structure

The repository is organized to strictly separate the presentation layer, the API orchestration layer, and the machine learning computational components.

- `backend/app.py`: The primary FastAPI application defining RESTful endpoints and request orchestration.
- `backend/benchmark.py`: Systematic benchmarking harness for measuring model latency and scoring distributions.
- `backend/models/`: Contains the fundamental deep learning architectures, notably the custom PyTorch implementation of the `Seq2SeqLSTM`.
- `backend/pipeline/`: Encapsulates inference logic modules, including the `bart_summarizer`, `clinical_ner`, and `rouge_eval` metric calculators.
- `backend/train/`: Houses the training and fine-tuning routines (`train_lstm.py`, `train_bart.py`) for the respective models.
- `backend/utils/`: Provides utility functions for document ingestion (`file_extractor`) and algorithmic text segmentation (`rag_chunker`).
- `frontend-react/`: The modern, component-driven React application serving as the primary user interface.

## Model Details and Evaluation

The summarization engine utilizes `facebook/bart-large-cnn` as its primary transformer, while the clinical entity extraction is powered by `samrawal/bert-base-uncased_clinical-ner`, a model specifically fine-tuned on the i2b2 clinical dataset. Evaluation is conducted using the standard Recall-Oriented Understudy for Gisting Evaluation (ROUGE) metrics. The system calculates ROUGE-1 (unigram overlap), ROUGE-2 (bigram overlap), and ROUGE-L (longest common subsequence) by comparing the model's generated summaries against ground-truth reference texts. The inclusion of the custom LSTM sequence model allows researchers to quantitatively observe the performance delta introduced by attention mechanisms during the ablation study.

## Usage Instructions

To utilize the platform, navigate to the React frontend dashboard and select the "End-to-End Analyzer" module. Users may upload clinical reports in standard documentation formats (PDF, DOCX) or directly input unstructured raw text. Upon initiating the analysis, the system will concurrently process the request through the summarization and NER pipelines. The resulting output displays the original text, the abstractive summary, processing metrics, and an interactive visualization of the extracted medical entities categorized by taxonomy.

## Limitations and Assumptions

The current iteration of the pipeline operates under specific constraints. The summarization models are primarily trained and evaluated using the CNN/DailyMail dataset as a structural proxy. While this develops robust abstractive capabilities, there remains a domain gap when processing highly specialized medical taxonomy. Additionally, the system assumes that the ingested text follows standard English clinical narrative structures. Highly fragmented data, such as unstructured laboratory tables or raw shorthand notes, may result in degraded entity extraction recall and summarization coherence.

## Future Improvements

Future iterations will focus on eliminating the domain gap by executing full-scale fine-tuning protocols on specialized medical datasets, such as MIMIC-III or PubMed corpora. Furthermore, the architecture will be migrated from reliance on external inference APIs to fully localized, containerized model deployments to ensure strict adherence to HIPAA and general healthcare data privacy regulations. Subsequent optimizations will target latency reduction via model quantization and the implementation of asynchronous task queues (e.g., Celery) to support high-throughput, web-scale deployments.
