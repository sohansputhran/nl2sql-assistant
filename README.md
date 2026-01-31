# NL2SQL Assistant (Open-Source, Production-Oriented)

A **schema-aware Natural Language → SQL system** built using **open-source LLMs**, **RAG**, **Streamlit**, and **CI/CD**, developed incrementally using **Agile methodology**.

This project demonstrates how **real NL→SQL systems** should be built: safely, explainably, and with human-in-the-loop controls.

---

## Project Vision

Build a **Natural Language → SQL assistant** with **two clearly separated modes**:

### 1. DB-Aware NL → SQL (Executable)
- Converts natural language into SQL that matches a known database schema
- Uses extracted schema (no hallucinated tables/columns)
- Supports safe execution (SELECT-only by default)

### 2. Generic NL → SQL (Non-Executable)
- Converts any natural language into SQL
- Not tied to a database
- Supports multiple SQL dialects
- Intended for learning, drafting, and prototyping

---

## Core Capabilities

### DB-Aware NL → SQL
```
Natural Language
 -> Schema Injection
 -> Open-Source LLM
 -> SQL Validation
 -> Risk Classification
 -> Execute & Visualize
```

### Generic NL → SQL
```
Natural Language
 -> Dialect-Aware Prompt
 -> Open-Source LLM
 -> SQL Output (not executed)
```

---

## Write Mode (RAG + Human-in-the-Loop)

Write operations are intentionally isolated for safety.

Features:
- Intent detection (read vs write)
- RAG grounding (schema + data dictionary)
- JSON-only SQL generation
- Hard validation rules
- Transactional execution
- Automatic DB backups
- Explicit user confirmation

---

## Agile Delivery Stages

- Stage 0: Foundation & CI/CD
- Stage 1: Schema Explorer
- Stage 2: DB-Aware NL → SQL (Read)
- Stage 3: Guardrails & Risk Classification
- Stage 4: UX & Explainability
- Stage 5: Write Mode with RAG
- **Stage 6: Dual-Mode NL → SQL (DB-aware + Generic)**

---

## Tech Stack

- Python 3.11
- Streamlit
- SQLite
- LangChain
- Ollama (open-source LLMs)
- RAG (BM25)
- Ruff
- Pytest
- GitHub Actions

---

## Running Locally

```bash
pip install -r requirements.txt
ollama serve
ollama pull llama3.1
streamlit run app/Home.py
```

---