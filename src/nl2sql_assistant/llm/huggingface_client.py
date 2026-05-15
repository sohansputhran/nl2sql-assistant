import os
import requests
from typing import Optional

def _get_api_token() -> str:
    """
    Resolve HuggingFace API token.
    Priority: Streamlit secrets -> env var HUGGINGFACE_API_TOKEN
    """
    try:
        import streamlit as st
        token = st.secrets.get("HUGGINGFACE_API_TOKEN", "")
        if token:
            return token
    except Exception:
        pass
    return os.getenv("HUGGINGFACE_API_TOKEN", "")


def get_hf_model(
    model_id: str = "defog/sqlcoder-7b-2",
    temperature: float = 0.01,
    max_new_tokens: int = 500,
):
    """
    Returns a LangChain-compatible HuggingFaceEndpoint.

    This is a drop-in replacement for get_chat_model() from the Ollama client.
    It plugs directly into LangChain chains: prompt | get_hf_model() | StrOutputParser()
    """
    from langchain_community.llms import HuggingFaceEndpoint  # lazy import

    token = _get_api_token()
    if not token:
        raise RuntimeError(
            "HuggingFace API token not found. "
            "Set HUGGINGFACE_API_TOKEN in .streamlit/secrets.toml or as an env var."
        )

    return HuggingFaceEndpoint(
        repo_id=model_id,
        huggingfacehub_api_token=token,
        task="text-generation",
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        do_sample=False,
    )


class HuggingFaceClient:
    """Client for HuggingFace Inference API."""
    
    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token or os.getenv("HUGGINGFACE_API_TOKEN")
        self.model_id = "defog/sqlcoder-7b-2"
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
        self.headers = {"Authorization": f"Bearer {self.api_token}"}
    
    def generate_sql(
        self, 
        prompt: str, 
        max_tokens: int = 500,
        temperature: float = 0.0  # Deterministic for SQL
    ) -> str:
        """
        Generate SQL from natural language using HF Inference API.
        
        Args:
            prompt: Formatted prompt with schema + question
            max_tokens: Max tokens to generate
            temperature: 0.0 for deterministic SQL generation
        
        Returns:
            Generated SQL query string
        """
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "return_full_text": False,
                "do_sample": False  # Greedy decoding for SQL
            }
        }
        
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            # HF returns list of dicts with 'generated_text'
            sql = result[0]["generated_text"]
            return self._extract_sql(sql)
        elif response.status_code == 503:
            # Model is loading, wait and retry
            raise ModelLoadingError("Model is loading, try again in 20s")
        else:
            raise HuggingFaceAPIError(
                f"API error {response.status_code}: {response.text}"
            )
    
    def _extract_sql(self, text: str) -> str:
        """Extract SQL from model output."""
        # SQLCoder outputs: "The following SQL query..."
        if "```sql" in text:
            # Extract from code block
            sql = text.split("```sql")[1].split("```")[0].strip()
        elif "SELECT" in text.upper():
            # Find first SELECT statement
            sql = text[text.upper().find("SELECT"):].strip()
        else:
            sql = text.strip()
        
        return sql

class ModelLoadingError(Exception):
    """Model is still loading on HF servers."""
    pass

class HuggingFaceAPIError(Exception):
    """General HF API error."""
    pass