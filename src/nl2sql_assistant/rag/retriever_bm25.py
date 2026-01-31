from __future__ import annotations

import re
from dataclasses import dataclass

from rank_bm25 import BM25Okapi

from nl2sql_assistant.rag.corpus import RagCorpus

_TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


def _tokenize(text: str) -> list[str]:
    # Tokenization kept simple and transparent for portfolio readability.
    return _TOKEN_RE.findall(text.lower())


@dataclass
class RagIndex:
    """
    BM25 index over corpus chunks.

    - No model downloads (CI-safe)
    - Still delivers strong “retrieve relevant context” behavior
    """

    corpus: RagCorpus
    bm25: BM25Okapi
    tokenized_chunks: list[list[str]]


def build_index(corpus: RagCorpus) -> RagIndex:
    tokenized = [_tokenize(c) for c in corpus.chunks]
    bm25 = BM25Okapi(tokenized)
    return RagIndex(corpus=corpus, bm25=bm25, tokenized_chunks=tokenized)


def retrieve(index: RagIndex, query: str, k: int = 3) -> str:
    """
    Returns top-k retrieved chunks concatenated.
    The returned string is fed into the write-SQL prompt.
    """
    q_tokens = _tokenize(query)
    scores = index.bm25.get_scores(q_tokens)

    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    chunks = [index.corpus.chunks[i] for i in ranked if scores[i] > 0]

    # If nothing matches, return full schema (safe fallback).
    if not chunks:
        return "\n\n---\n\n".join(index.corpus.chunks[: min(2, len(index.corpus.chunks))])

    return "\n\n---\n\n".join(chunks)
