"""Configuration for available models and vision processing parameters."""

from dataclasses import dataclass
from typing import List

# Vision model defaults
DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_TOKENS = 2000
DEFAULT_PROMPT = "Describe this image in detail"

# Image processing
SUPPORTED_IMAGE_TYPES = ("jpg", "jpeg", "png", "gif", "webp")
IMAGE_MIME_TYPE = "image/jpeg"


@dataclass
class ModelConfig:
    """Configuration for available models from different providers."""

    OPENAI_TEXT_MODELS = ["openai/gpt-4o", "openai/gpt-4o-mini"]
    OLLAMA_TEXT_MODELS = ["ollama/llama3.2", "ollama/phi4"]
    GEMINI_TEXT_MODELS = ["gemini/gemini-2.5-flash", "gemini/gemini-2.5-flash-lite"]
    PERPLEXITY_TEXT_MODELS = ["perplexity/sonar", "perplexity/sonar-pro"]

    OPENAI_VISION_MODELS = ["openai/gpt-4o", "openai/gpt-4o-mini"]
    OLLAMA_VISION_MODELS = ["ollama/llava", "ollama/llava-llama3", "ollama/bakllava"]
    GEMINI_VISION_MODELS = ["gemini/gemini-2.5-flash", "gemini/gemini-2.5-flash-lite"]

    TEXT_MODELS = OPENAI_TEXT_MODELS + OLLAMA_TEXT_MODELS + GEMINI_TEXT_MODELS + PERPLEXITY_TEXT_MODELS
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
