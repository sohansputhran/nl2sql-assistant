# NL2SQL Assistant (Open‑Source, Production‑Oriented)

A **schema‑aware Natural Language → SQL system** built using **open‑source LLMs**, **RAG**, **Streamlit**, and **CI/CD**, developed step‑by‑step using **Agile methodology**.

This project goes beyond demos and focuses on **safe, explainable, human‑in‑the‑loop AI for databases**.

---

## Project Vision

Build a **real‑world NL → SQL assistant** that:

- Converts natural language into **SQL queries (read + write)**
- Uses **open‑source LLMs only** (via Ollama)
- Applies **guardrails, validation, and risk classification**
- Uses **RAG** to ground database write operations
- Requires **explicit human confirmation** before data modification
- Is fully deployable with **Streamlit**
- Follows **Agile development, CI/CD, and testing best practices**

---

## Current Status

### ✅ Stage 0 – Foundation
- Streamlit application skeleton
- Ruff linting & formatting
- Pytest test suite
- GitHub Actions CI pipeline

### ✅ Stage 1 – SQLite Schema Explorer
- Sample SQLite database
- Prompt‑ready schema extraction
- Schema Explorer UI
- SELECT‑only query runner

### ✅ Stage 2 – NL → SQL (Read Queries)
- Open‑source LLM adapter (Ollama)
- Few‑shot PromptTemplates
- Schema‑aware SQL generation
- SELECT‑only hard validation

### ✅ Stage 3 – Guardrails & Risk Classification
- LLM‑as‑critic pattern
- Structured JSON risk output
- Risk levels: low / medium / high

### ✅ Stage 4 – UX & Explainability
- Auto‑run risk checks
- Natural language SQL explanation
- Optional SQL auto‑fix

### ✅ Stage 5 – Write Mode with RAG
- Intent‑aware write pipeline
- RAG‑grounded SQL generation
- Strict validation + transactions
- Database backup & rollback
- Human‑in‑the‑loop confirmation

---

## 🧱 Tech Stack
- Python 3.11
- Streamlit
- SQLite
- LangChain
- Ollama
- RAG (BM25)
- Ruff
- Pytest
- GitHub Actions

---

## Run Locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt

pytest -q
ruff check .
ruff format .

ollama serve
ollama pull llama3.1

streamlit run app/Home.py
```
