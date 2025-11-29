"""Configuration for available models organized by provider."""

from dataclasses import dataclass
from typing import List


@dataclass
class ModelConfig:
    """Configuration for available models from different providers."""

    OPENAI_TEXT_MODELS = ["openai/gpt-4o", "openai/gpt-4o-mini"]
    OLLAMA_TEXT_MODELS = ["ollama/llama3.2", "ollama/phi4"]
    GEMINI_TEXT_MODELS = [
        "gemini/gemini-2.0-flash",
        "gemini/gemini-2.0-flash-lite-preview-02-05",
        "gemini/gemini-2.0-pro-exp-02-05",
        "gemini/gemini-2.0-flash-thinking-exp-01-21",
    ]

    OPENAI_VISION_MODELS = ["openai/gpt-4o", "openai/gpt-4o-mini"]
    OLLAMA_VISION_MODELS = ["ollama/llava", "ollama/llava-llama3", "ollama/bakllava"]
    GEMINI_VISION_MODELS = [
        "gemini/gemini-2.0-flash",
        "gemini/gemini-2.0-flash-lite-preview-02-05",
        "gemini/gemini-2.0-pro-exp-02-05",
        "gemini/gemini-2.0-flash-thinking-exp-01-21",
    ]

    TEXT_MODELS = OPENAI_TEXT_MODELS + OLLAMA_TEXT_MODELS + GEMINI_TEXT_MODELS
    VISION_MODELS = OPENAI_VISION_MODELS + OLLAMA_VISION_MODELS + GEMINI_VISION_MODELS

    @classmethod
    def get_model(cls, index: int, model_type: str = "text"):
        """Get a model by index with validation.

        Args:
            index: Index of the model
            model_type: Type of model ('text' or 'vision')

        Returns:
            Model name if valid, None otherwise
        """
        models = cls.TEXT_MODELS if model_type == "text" else cls.VISION_MODELS
        if 0 <= index < len(models):
            return models[index]
        return None

    @classmethod
    def get_models(cls, model_type: str = "text") -> List[str]:
        """Get all models of a specific type.

        Args:
            model_type: Type of model ('text' or 'vision')

        Returns:
            List of available models
        """
        return cls.TEXT_MODELS if model_type == "text" else cls.VISION_MODELS
