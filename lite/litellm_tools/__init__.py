"""LiteLLM Tools - Multi-provider LLM and Vision API interaction library."""

from .logging_config import configure_logging
from .config import ModelConfig
from .text import LiteText, LiteTextResponse
from .vision import LiteVision

# Configure logging to file only on import
configure_logging(log_file="litellm.log")

__all__ = [
    "ModelConfig",
    "LiteText",
    "LiteTextResponse",
    "LiteVision",
]
