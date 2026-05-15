from enum import Enum
import os

class LLMBackend(Enum):
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"

class Config:
    # LLM Backend
    LLM_BACKEND = LLMBackend.HUGGINGFACE  # Switch from OLLAMA
    
    # HuggingFace
    HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
    HUGGINGFACE_MODEL = "defog/sqlcoder-7b-2"
    
    # Ollama (legacy, for local dev)
    OLLAMA_BASE_URL = "http://localhost:11434"
    OLLAMA_MODEL = "llama3.1"