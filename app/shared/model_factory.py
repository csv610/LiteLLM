"""
model_factory.py - Unified model factory for all AI frameworks.

Usage:
    from app.shared.model_factory import get_model, get_structured_model

    # Basic model (text output)
    llm = get_model("gpt-4", framework="langchain")

    # Structured model (Pydantic output)
    structured_llm = get_structured_model("gpt-4", framework="langchain", response_schema=MyModel)
"""

import os
from typing import Optional, Type, Union, Any
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_litellm import ChatLiteLLM
from agno.models.google import Gemini
from agno.models.ollama import Ollama

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

LITELLM_PROVIDER_ALIASES = {
    "anthropic": "anthropic",
    "cohere": "cohere",
    "ai21": "ai21",
    "azure": "azure",
    "bedrock": "bedrock",
    "sagemaker": "sagemaker",
    "vertex_ai": "vertex_ai",
    "vllm": "vllm",
    "sambastudio": "sambastudio",
    "marqo": "marqo",
    "ollama": "ollama",
    "openai": "openai",
}


def get_model(
    model_name: str,
    framework: str = "langchain",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    litellm_provider: Optional[str] = None,
) -> Union[ChatOpenAI, ChatGoogleGenerativeAI, ChatOllama, ChatLiteLLM, Gemini, Ollama]:
    """
    Unified model factory that returns the appropriate model instance
    based on the model name and framework.
    """
    model_name_lower = model_name.lower()
    is_openrouter = "openrouter" in model_name_lower
    is_litellm = framework == "litellm" or litellm_provider is not None

    if framework in ("langchain", "langgraph"):
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
        elif "gpt" in model_name_lower or "claude" in model_name_lower:
            return ChatOpenAI(
                model=model_name, temperature=temperature, max_tokens=max_tokens
            )
        else:
            return ChatOllama(
                model=model_name, temperature=temperature, max_tokens=max_tokens
            )

    elif framework == "agno":
        if is_openrouter:
            return Ollama(
                id=model_name.replace("openrouter/", ""),
                temperature=temperature,
                max_tokens=max_tokens,
            )
        elif "gemini" in model_name_lower:
            return Gemini(id=model_name, temperature=temperature, max_tokens=max_tokens)
        else:
            return Ollama(id=model_name, temperature=temperature, max_tokens=max_tokens)

    elif framework == "litellm":
        return ChatLiteLLM(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            provider=litellm_provider,
        )

    else:
        raise ValueError(f"Unsupported framework: {framework}")


def get_structured_model(
    model_name: str,
    framework: str = "langchain",
    response_schema: Optional[Type[BaseModel]] = None,
    temperature: float = 0.3,
    max_tokens: Optional[int] = None,
    litellm_provider: Optional[str] = None,
) -> Any:
    """
    Returns a model configured for structured Pydantic output.

    Args:
        model_name: Model identifier
        framework: "langchain", "langgraph", or "litellm"
        response_schema: Pydantic model class for structured output
        temperature: Lower temperature for structured output (default: 0.3)
        max_tokens: Optional max tokens
        litellm_provider: LiteLLM provider override

    Returns:
        Structured model instance with .invoke() returning Pydantic objects
    """
    if response_schema is None:
        raise ValueError(
            "response_schema (Pydantic model) is required for structured output"
        )

    model_name_lower = model_name.lower()
    is_openrouter = "openrouter" in model_name_lower
    is_litellm = framework == "litellm" or litellm_provider is not None

    if framework in ("langchain", "langgraph"):
        if is_litellm:
            base_model = ChatLiteLLM(
                model=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                provider=litellm_provider,
            )
        elif is_openrouter:
            if not OPENROUTER_API_KEY:
                raise ValueError("OPENROUTER_API_KEY environment variable not set")
            base_model = ChatOpenAI(
                model=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                base_url=OPENROUTER_BASE_URL,
                api_key=OPENROUTER_API_KEY,
            )
        elif "gemini" in model_name_lower:
            base_model = ChatGoogleGenerativeAI(
                model=model_name, temperature=temperature, max_tokens=max_tokens
            )
        elif "gpt" in model_name_lower or "claude" in model_name_lower:
            base_model = ChatOpenAI(
                model=model_name, temperature=temperature, max_tokens=max_tokens
            )
        else:
            base_model = ChatOllama(
                model=model_name, temperature=temperature, max_tokens=max_tokens
            )

        return base_model.with_structured_output(response_schema)

    elif framework == "litellm":
        base_model = ChatLiteLLM(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            provider=litellm_provider,
        )
        return base_model.with_structured_output(response_schema)

    elif framework == "agno":
        if is_openrouter:
            base_model = Ollama(
                id=model_name.replace("openrouter/", ""),
                temperature=temperature,
                max_tokens=max_tokens,
            )
        elif "gemini" in model_name_lower:
            base_model = Gemini(
                id=model_name, temperature=temperature, max_tokens=max_tokens
            )
        else:
            base_model = Ollama(
                id=model_name, temperature=temperature, max_tokens=max_tokens
            )

        if hasattr(base_model, "with_structured_output"):
            return base_model.with_structured_output(response_schema)
        else:
            raise ValueError(
                "Agno Ollama does not support structured output. Use LangChain instead."
            )

    else:
        raise ValueError(f"Unsupported framework: {framework}")


__all__ = ["get_model", "get_structured_model", "LITELLM_PROVIDER_ALIASES"]
