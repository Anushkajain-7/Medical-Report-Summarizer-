# Medical Report Intelligence Platform

Built by Sai Venkat and Anushka Jain.

## Overview
This platform is an advanced clinical reasoning assistant that transforms unstructured medical reports into clear, actionable intelligence. Using a combination of custom Deep Learning models and state-of-the-art NLP transformers, the system interprets medical narratives, identifies clinical patterns, and provides structured care guidance.

## Key Features
- Narrative-Aware Reasoning: Understands the "story" behind medical reports, not just keywords.
- Clinical NER: Automatically extracts Diseases, Medications, Symptoms, and Treatments using BioClinicalBERT.
- Intelligent Summarization: Generates professional-grade technical abstracts using BART and custom LSTM architectures.
- Severity Triage: Detects critical medical events (e.g., vascular emergencies) and provides prioritized safety alerts.
- Care Guidance: Provides domain-specific next steps, including lifestyle and nutritional advice.

## Installation and Setup

### 1. Backend Configuration
The backend requires Python 3.9+ and a Hugging Face API token.
```bash
cd backend
python -m venv venv
source venv/bin/activate # Use venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Create a `.env` file in the `backend` folder:
```env
HF_API_TOKEN=your_huggingface_token_here
```

### 2. Frontend Configuration
The frontend is built with React and Vite.
```bash
cd frontend-react
npm install
```

## Running the Project
The project is designed to be launched with a single command. From the root directory, run:
```bash
.\run.bat
```
- Frontend: http://localhost:5173
- Backend: http://localhost:8000

## Technical Documentation
For a detailed explanation of our Deep Learning architectures, LSTM implementation, and NLP pipelines, please refer to:
[NLP_DEEP_LEARNING.md](NLP_DEEP_LEARNING.md)
