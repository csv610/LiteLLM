"""
model_factory.py - Unified model factory for MedKit with Pydantic support.
"""

import os
from typing import Optional, Type, Union
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_litellm import ChatLiteLLM
from agno.models.google import Gemini
from agno.models.ollama import Ollama

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def get_chain_model(
    model_name: str,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    litellm_provider: Optional[str] = None,
) -> Union[ChatOpenAI, ChatGoogleGenerativeAI, ChatOllama, ChatLiteLLM]:
    """LangChain model factory with OpenRouter and LiteLLM support."""
    model_name_lower = model_name.lower()
    is_openrouter = "openrouter" in model_name_lower
    is_litellm = litellm_provider is not None

    if is_litellm:
        return ChatLiteLLM(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            provider=litellm_provider,
        )
    elif is_openrouter:
        if not OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            base_url=OPENROUTER_BASE_URL,
            api_key=OPENROUTER_API_KEY,
        )
    elif "gemini" in model_name_lower:
        return ChatGoogleGenerativeAI(
            model=model_name, temperature=temperature, max_tokens=max_tokens
        )
    elif "gpt" in model_name_lower:
        return ChatOpenAI(
            model=model_name, temperature=temperature, max_tokens=max_tokens
        )
    else:
        return ChatOllama(
            model=model_name, temperature=temperature, max_tokens=max_tokens
        )


def get_agno_model(
    model_name: str,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> Union[Gemini, Ollama]:
    """Agno model factory with OpenRouter support."""
    model_name_lower = model_name.lower()
    is_openrouter = "openrouter" in model_name_lower

    if is_openrouter:
        return Ollama(id=model_name.replace("openrouter/", ""))
    elif "gemini" in model_name_lower:
        return Gemini(id=model_name, temperature=temperature, max_tokens=max_tokens)
    else:
        return Ollama(id=model_name, temperature=temperature, max_tokens=max_tokens)


def get_chain_model_structured(
    model_name: str,
    response_schema: Optional[Type[BaseModel]] = None,
    temperature: float = 0.3,
    max_tokens: Optional[int] = None,
    litellm_provider: Optional[str] = None,
) -> Union[ChatOpenAI, ChatGoogleGenerativeAI, ChatOllama, ChatLiteLLM]:
    """
    Returns a LangChain model configured for structured Pydantic output.
    """
    if response_schema is None:
        raise ValueError("response_schema (Pydantic model) is required")

    base_model = get_chain_model(
        model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        litellm_provider=litellm_provider,
    )

    return base_model.with_structured_output(response_schema)


__all__ = ["get_chain_model", "get_agno_model", "get_chain_model_structured"]
