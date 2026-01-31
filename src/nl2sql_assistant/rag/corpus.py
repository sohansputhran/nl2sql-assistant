from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RagCorpus:
    """
    Stores text chunks used for retrieval.

    - We keep chunks relatively small and readable.
    - Later you can add chunking by headings or sentences if corpus grows.
    """

    chunks: list[str]


def _chunk_text(text: str, max_chars: int = 900) -> list[str]:
    """
    Very simple chunker to keep contexts compact.
    Chunking makes retrieval more precise and keeps LLM context smaller.
    """
    text = text.strip()
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    buf: list[str] = []
    size = 0

    for line in text.splitlines():
        if size + len(line) + 1 > max_chars and buf:
            chunks.append("\n".join(buf).strip())
            buf, size = [], 0
        buf.append(line)
        size += len(line) + 1

    if buf:
        chunks.append("\n".join(buf).strip())

    return [c for c in chunks if c]


def build_corpus(schema_text: str, dictionary_path: Path | None = None) -> RagCorpus:
    """
    Corpus = schema + optional data dictionary.
    You can add more docs later (policies, examples, business definitions).
    """
    chunks: list[str] = []
    chunks.extend(_chunk_text(schema_text))

    if dictionary_path and dictionary_path.exists():
        dictionary_text = dictionary_path.read_text(encoding="utf-8").strip()
        if dictionary_text:
            chunks.extend(_chunk_text(dictionary_text))

    return RagCorpus(chunks=chunks)
