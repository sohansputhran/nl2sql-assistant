# 🧠 NL2SQL Assistant (Open-Source)

A **schema-aware Natural Language → SQL assistant** built using **open-source LLMs**, **Streamlit**, and **CI/CD**, developed incrementally using **Agile methodology**.

---

## 🚀 Project Vision
Build a **production-grade NL → SQL system** that:
- Generates safe, executable SQL from natural language
- Uses **open-source LLMs only**
- Applies **guardrails & risk classification**
- Is fully deployable with **Streamlit**
- Follows **Agile + CI/CD best practices**

---

## 🧱 Tech Stack
- Python 3.11
- Streamlit
- SQLite
- LangChain
- Ollama (open-source LLMs)
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
