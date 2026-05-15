# LLM Factory 

from typing import Protocol
from .huggingface_client import HuggingFaceClient
from .ollama_client import OllamaClient  # Keep for local dev

class LLMClient(Protocol):
    """Protocol for LLM clients."""
    
    def generate_sql(self, prompt: str, **kwargs) -> str:
        """Generate SQL from prompt."""
        ...

def get_llm_client(backend: str = "huggingface") -> LLMClient:
    """
    Factory function to get appropriate LLM client.
    
    This allows easy switching between backends for:
    - Production: HuggingFace
    - Local dev: Ollama
    - Testing: Mock client
    """
    if backend == "huggingface":
        return HuggingFaceClient()
    elif backend == "ollama":
        return OllamaClient()
    elif backend == "mock":
        return MockLLMClient()
    else:
        raise ValueError(f"Unknown backend: {backend}")