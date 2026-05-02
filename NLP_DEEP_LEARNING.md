# Clinical NLP and Deep Learning Architecture

This project leverages advanced Natural Language Processing (NLP) and Deep Learning techniques to transform unstructured medical text into structured, actionable clinical intelligence.

## 1. Deep Learning Architectures

### Custom Seq2Seq LSTM with Attention
We implemented a custom Recurrent Neural Network (RNN) architecture using PyTorch for foundational sequence modeling:
- Encoder-Decoder Framework: A two-layer stacked bidirectional LSTM serves as the encoder to capture long-range dependencies in medical narratives.
- Bahdanau Attention: An additive attention mechanism is integrated to allow the decoder to focus on specific segments of the input text during summary generation, mitigating the information bottleneck of standard LSTMs.
- Purpose: This architecture provides a robust baseline for sequence-to-sequence tasks and allows for rigorous ablation studies on attention-based focus.

### Transformer-Based Summarization (BART)
For state-of-the-art abstractive summarization, the pipeline utilizes Facebook's BART (Bidirectional and Auto-Regressive Transformers):
- Architecture: BART uses a standard seq2seq transformer architecture with a bidirectional encoder and a GPT-like autoregressive decoder.
- Clinical Utility: It is particularly effective at "denoising" unstructured reports and regenerating them as coherent, grammatically correct clinical narratives.

## 2. Clinical Natural Language Processing

### Clinical Named Entity Recognition (NER)
To structure medical data, we utilize BioClinicalBERT:
- Model: A domain-specific masked language model (MLM) fine-tuned on clinical datasets (i2b2).
- Extraction: The system extracts four primary taxonomies:
    1. Diseases and Conditions
    2. Medications and Dosages
    3. Symptoms and Observations
    4. Medical Procedures and Treatments
- Hybrid Logic: We augment the neural NER with a massive, high-precision clinical keyword dictionary to ensure reliability even when language models encounter highly technical or rare terminology.

### Clinical Reasoning and Pattern Inference
Beyond simple extraction, the project implements a deterministic reasoning layer:
- Pattern Analysis: The system evaluates the relationships between extracted entities to identify dominant clinical stories (e.g., Cardiac vs. Infection).
- Severity Triage: Deep learning findings are scored against clinical heuristics to classify reports as Normal, Mild, Moderate, Serious, or Critical.
- Priority Override: Life-threatening indicators (like "hemorrhage" or "rupture") are elevated using a priority-based logic gate to ensure critical findings are never suppressed by generic summaries.

## 3. Evaluation Framework
- ROUGE Metric Suite: Generated summaries are mathematically evaluated against reference texts using ROUGE-1 (unigrams), ROUGE-2 (bigrams), and ROUGE-L (Longest Common Subsequence).
- Latency Benchmarking: System performance is tracked through a benchmarking harness that measures the inference time of both LSTM and Transformer architectures.
