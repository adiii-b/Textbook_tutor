# 📘Offline Textbook Chatbot (Low-Resource System)
## Objective
Build a fully offline chatbot system that:
- Runs on low-end CPUs (i3/i5, no GPU)
- Works without internet
- Responds within ≤ 3 seconds
- Can:
  - Display textbook content reliably (no hallucination)
  - Explain concepts simply using an LLM
---
## Core Design Principle
Use the LLM for reasoning, not storage.
- Textbook content → stored explicitly (retrieval)
- LLM → used only for explanation/summarization
---
## System Architecture
User Input
    ↓
Query Router
    ↓
Retriever (Textbook chunks)
    ↓
+-----------------------------+
| Mode 1: Show Text (Direct)  |
| Mode 2: Explain (LLM)       |
+-----------------------------+
    ↓
Response
---
## Tech Stack
### LLM Inference
- llama.cpp (CPU optimized)
- Model:
  - Phi-3 Mini OR Gemma 2B
  - Quantized (.gguf, Q4_K_M recommended)

### Backend
- Python (FastAPI or CLI)

### Retrieval
- Option A (recommended): BM25 / keyword search
- Option B (optional): sentence-transformers (MiniLM)

### Storage
- JSON or SQLite
---
## Textbook Processing Pipeline
### Step 1: Extract Text
- PDF → PyMuPDF or pdfplumber
- Images → Tesseract OCR
---
### Step 2: Clean Text
- Remove headers/footers
- Remove page numbers
- Remove formatting artifacts
---
### Step 3: Chunking
Rules:
- 150–300 words per chunk
- Preserve semantic meaning
Example:
{
  "id": 1,
  "chapter": "Electricity",
  "section": "Ohm's Law",
  "content": "Ohm’s law states that the current through a conductor..."
}
---
### Step 4: Indexing
Option A: Keyword Search (Preferred)
- Use BM25 or TF-IDF
- Libraries: rank_bm25
Option B: Embeddings (Optional)
- Model: all-MiniLM-L6-v2
- Store vectors in-memory
---
## Retrieval Logic
def retrieve(query):
    results = search_index(query)
    return top_k(results, k=2)

Constraints:
- top_k = 1 or 2
- Context < 300–400 tokens
---

## LLM Integration

### Model Requirements
- ≤ 4B parameters
- Quantized (.gguf)
- Loaded once at startup
---
### Prompt Template
Context:
{retrieved_text}

Question:
{user_query}

Task:
Explain this simply in 3–4 bullet points.
---

### Generation Parameters

max_tokens = 60–80
temperature = 0.3–0.5
top_p = 0.9
---
## Performance Optimization

Critical Rules:
- Load model once
- Keep context small (≤ 2 chunks)
- Limit output length
- Optional: stream output
---
### Expected Latency

Retrieval: ~10–50 ms  
Prompt prep: negligible  
LLM generation: ~1.5–2.5 s  
Total: ~2–3 seconds  
---
## Query Routing Logic

def route_query(query):
    if "show" in query or "display" in query:
        return "retrieval_only"
    else:
        return "explain"

---

## Mode 1: Show Text

def show_text(query):
    chunks = retrieve(query)
    return chunks[0]["content"]

- Instant
- No hallucination

---
## Mode 2: Explain
def explain(query):
    chunks = retrieve(query)
    context = combine(chunks)
    prompt = build_prompt(context, query)
    return llm.generate(prompt)
---
## Minimal API Design
POST /chat

Request:
{
  "query": "Explain Ohm's law"
}

Response:
{
  "mode": "explain",
  "answer": "..."
}
---
## Project Structure

project/
│
├── data/
│   ├── textbook.json
│
├── retriever/
│   ├── index.py
│   ├── search.py
│
├── llm/
│   ├── model_loader.py
│   ├── inference.py
│
├── api/
│   ├── main.py
│
├── utils/
│   ├── chunking.py
│   ├── preprocessing.py
│
└── README.md
---
## Constraints & Non-Goals

- No internet usage
- No GPU dependency
- No models >4B
- No heavy vector DB
- No long responses
---
## Success Criteria
- Response time ≤ 3 seconds
- Accurate textbook retrieval
- No hallucination in show mode
- Clear explanations
- Runs on low-end CPU
---
## Optional Enhancements
- Simple web UI
- Highlight retrieved text
- Multi-language support
- Offline voice support
- Query caching
---
## Summary
- Retrieval ensures accuracy
- Small LLM ensures understanding
- Quantization ensures speed

## Guiding Principle
You're not just a coding assistant — you're my teacher.
For every suggestion:
1. Explain the underlying concept or principle
2. Explain WHY this approach is better than alternatives
3. Mention at least one alternative and why it’s worse here
4. Walk through the logic step-by-step
5. Only then show the code

Assume I am learning and want deep understanding, not just working code