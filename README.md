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

## Tech Stack
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
