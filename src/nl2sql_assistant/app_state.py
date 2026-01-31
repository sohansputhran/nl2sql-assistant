from __future__ import annotations

from pathlib import Path

import streamlit as st

from nl2sql_assistant.db.bootstrap import ensure_sample_db
from nl2sql_assistant.db.schema import schema_as_text
from nl2sql_assistant.rag.corpus import build_corpus
from nl2sql_assistant.rag.retriever_bm25 import RagIndex, build_index


@st.cache_resource
def get_db_path() -> Path:
    """
    Cache DB initialization so it happens once per app session.
    """
    db_path = Path("data/sample.db")
    ensure_sample_db(db_path)
    return db_path


@st.cache_resource
def get_rag_index() -> tuple[RagIndex, str]:
    """
    Build RAG index once at app start (cached).
    Returns:
      - RagIndex
      - schema_text (often useful to show or inject into prompts)
    """
    db_path = get_db_path()
    schema_text = schema_as_text(db_path)

    dictionary_path = Path("data/dictionary.md")
    corpus = build_corpus(schema_text=schema_text, dictionary_path=dictionary_path)
    index = build_index(corpus)

    return index, schema_text
