from __future__ import annotations

from dataclasses import dataclass

from langchain_ollama import ChatOllama


@dataclass(frozen=True)
class OllamaSettings:
    """
    Configuration for local open-source LLM usage via Ollama.

    For now, keeping it simple:
    - model: name installed in Ollama (e.g., llama3.1, mistral)
    - temperature: keep low for deterministic SQL output
    """

    model: str = "llama3.1"
    temperature: float = 0.1


def get_chat_model(settings: OllamaSettings | None = None) -> ChatOllama:
    """
    Returns a ChatOllama model instance.

    NOTE:
    - This requires Ollama running locally: `ollama serve`
    - And the model pulled: `ollama pull llama3.1`
    """
    s = settings or OllamaSettings()
    return ChatOllama(model=s.model, temperature=s.temperature)
