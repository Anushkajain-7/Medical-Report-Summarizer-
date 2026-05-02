Medical Report Intelligence Platform

Built by Sai Venkat and Anushka Jain.

Overview

The Medical Report Intelligence Platform is an advanced healthcare AI system designed to transform complex clinical reports into clear, structured, and actionable insights for end users.

Instead of simply summarizing text, this system performs clinical reasoning, interprets medical narratives, detects key health patterns, and provides practical guidance such as what the report means, what actions to take, and what precautions to follow.

The goal is to bridge the gap between technical medical data and human understanding.

Problem Statement

Medical reports are often difficult for non-medical users to understand. They contain complex terminology, raw lab values, and fragmented clinical observations.

This platform solves that problem by interpreting the report like a human expert, simplifying medical language, and generating structured insights and actionable guidance.

What This System Does

The system accepts medical reports in PDF, DOCX, or TXT format. It extracts and processes clinical text, performs summarization using BART and LSTM models, and applies Clinical Named Entity Recognition using BioClinicalBERT. It then analyzes the report context, identifies conditions and severity, and generates human-readable explanations along with guidance such as what to do, what to avoid, dietary suggestions, and warning signs.

Key Features

Narrative-Aware Reasoning: Understands the complete clinical story instead of relying only on keywords.

Clinical NER: Extracts Diseases, Drugs, Symptoms, and Treatments using BioClinicalBERT.

Intelligent Summarization: Uses BART and custom LSTM models to generate structured summaries.

Severity Detection: Identifies critical medical conditions and prioritizes risk.

Actionable Guidance: Provides clear next steps including lifestyle recommendations, diet suggestions, and precautions.

Tech Stack

Backend: FastAPI, Python
NLP Models: BART, BioClinicalBERT, LSTM Seq2Seq
Frontend: React (Vite) with Tailwind CSS
APIs: Hugging Face Inference API

Project Structure

Medical-Report-Summarizer--main/
backend/ – FastAPI backend
frontend-react/ – React frontend
api/ – API utilities
NLP_DEEP_LEARNING.md – Model documentation
requirements.txt
run.bat (optional)

Installation and Setup
Prerequisites

Python 3.9 to 3.11
Node.js (v16 or higher)
npm

Backend Setup

Navigate to backend folder:

cd backend

Create virtual environment:

python -m venv .venv

Activate environment (Windows):

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Environment Variables

Create a .env file inside the backend folder and add:

HF_API_TOKEN=your_huggingface_token_here

Frontend Setup

Navigate to frontend folder:

cd frontend-react

Install dependencies:

npm install

Running the Project (Recommended Method)
Start Backend

cd backend
uvicorn app:app --reload

If this fails, try:

uvicorn main:app --reload

Start Frontend (in a new terminal)

cd frontend-react
npm run dev

Access the Application

Frontend: http://localhost:5173

Backend: http://localhost:8000

Important Note

A run.bat file is included, but it may not work reliably depending on your environment or PowerShell configuration. It is recommended to run backend and frontend manually as shown above.

Output Format

For each uploaded report, the system generates:

Technical summary
Plain-language explanation
Detected conditions
Key findings
Recommended actions
Things to avoid
Diet guidance
Warning signs
Limitations

The system uses proxy datasets such as CNN/DailyMail for summarization. Clinical NER may not capture all rare or edge-case conditions. The guidance provided is informational and not a medical diagnosis.

Disclaimer

This system is for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.

Technical Documentation

Refer to NLP_DEEP_LEARNING.md for detailed explanation of models, architectures, and implementation.

