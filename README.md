# NL2SQL Assistant
Schema-aware Natural Language to SQL assistant using open-source LLMs, Streamlit, and CI/CD — built incrementally using Agile methodology.

---

## Project Vision
The goal of this project is to build a **real-world, production-quality NL → SQL assistant** that:
- Converts natural language questions into safe, executable SQL
- Uses **open-source LLMs only** (no paid APIs)
- Demonstrates **prompt engineering, classification, and guardrails**
- Is fully deployable via **Streamlit**
- Follows **Agile development with CI/CD and tests**

This project is designed to be **portfolio-ready** and recruiter-friendly.

---

## Tech Stack
- **Python 3.11**
- **Streamlit** – UI & deployment
- **SQLite** – Lightweight relational database
- **LangChain (planned)** – Prompt templates & chains
- **Open-source LLMs (planned)** – Ollama + LLaMA / Mistral
- **Ruff** – Linting & formatting
- **Pytest** – Testing
- **GitHub Actions** – CI/CD

---

## Repository Structure
```
nl2sql-assistant/
│
├── app/
│   ├── Home.py
│   └── pages/
│       └── 1_Schema_Explorer.py
│
├── src/
│   └── nl2sql_assistant/
│       ├── config.py
│       └── db/
│           ├── bootstrap.py
│           ├── schema.py
│           └── runner.py
│
├── data/
│   └── sample.db
│
├── tests/
│   ├── test_smoke.py
│   └── test_schema.py
│
├── .github/workflows/
│   └── ci.yml
│
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Running Locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt

pytest -q
ruff check .
ruff format .

streamlit run app/Home.py
```

---

## Agile Roadmap

- Stage 2: NL → SQL generation (PromptTemplates + open-source LLM)
- Stage 3: Guardrails & classification
- Stage 4: Full Streamlit UX + charts
- Stage 5: Deployment & documentation polish

---