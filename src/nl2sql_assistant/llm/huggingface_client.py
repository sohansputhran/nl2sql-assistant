import os
from typing import Any, List, Optional

from langchain_core.language_models.llms import LLM


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


class HuggingFaceInferenceLLM(LLM):
    """
    LangChain-compatible LLM that calls HuggingFace Inference API via
    huggingface_hub.InferenceClient.text_generation().

    This avoids the deprecated .post() method used by langchain-community and
    langchain-huggingface wrappers, which break with huggingface_hub >= 0.24.
    """

    model_id: str = "defog/sqlcoder-7b-2"
    max_new_tokens: int = 500
    temperature: float = 0.01
    api_token: str = ""

    @property
    def _llm_type(self) -> str:
        return "huggingface_inference"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
        from huggingface_hub import InferenceClient

        client = InferenceClient(model=self.model_id, token=self.api_token)
        result = client.text_generation(
            prompt,
            max_new_tokens=self.max_new_tokens,
            temperature=self.temperature,
            do_sample=False,
            stop_sequences=stop or [],
        )
        return result


def get_hf_model(
    model_id: str = "defog/sqlcoder-7b-2",
    temperature: float = 0.01,
    max_new_tokens: int = 500,
) -> HuggingFaceInferenceLLM:
    """
    Returns a LangChain-compatible LLM backed by HuggingFace Inference API.

    Drop-in replacement for get_chat_model() from the Ollama client.
    Plugs directly into LangChain chains: prompt | get_hf_model() | StrOutputParser()
    """
    token = _get_api_token()
    if not token:
        raise RuntimeError(
            "HuggingFace API token not found. "
            "Set HUGGINGFACE_API_TOKEN in .streamlit/secrets.toml or as an env var."
        )

    return HuggingFaceInferenceLLM(
        model_id=model_id,
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        api_token=token,
    )


class ModelLoadingError(Exception):
    """Model is still loading on HF servers."""
    pass


class HuggingFaceAPIError(Exception):
    """General HF API error."""
    pass