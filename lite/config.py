"""Configuration for available models and vision processing parameters."""

from dataclasses import dataclass
from typing import Optional, Union, List, Dict, Any
from pydantic import BaseModel

# Vision model defaults
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2000
DEFAULT_PROMPT = "Describe this image in detail"

# Image processing
SUPPORTED_IMAGE_TYPES = ("jpg", "jpeg", "png", "gif", "webp")
IMAGE_MIME_TYPE = "image/jpeg"


@dataclass
class ModelConfig:
    """Configuration for model interactions."""

    model: str
    temperature: float = DEFAULT_TEMPERATURE


@dataclass
class ChatConfig:
    """Configuration for chat session management."""

    max_history: int = 10
    auto_save: bool = False
    save_dir: str = "."


@dataclass
class ModelInput:
    """Input parameters for model interactions."""

    user_prompt: str = ""
    image_path: Optional[str] = None
    image_paths: Optional[list[str]] = None
    system_prompt: Optional[str] = None
    response_format: Optional[BaseModel] = None

    def __post_init__(self):
        """Validate input after initialization."""
        if not self.user_prompt or not self.user_prompt.strip():
            if not self.image_path and not self.image_paths:
                raise ValueError("user_prompt cannot be empty unless an image_path(s) is provided")

        # Normalize empty system_prompt to None
        if self.system_prompt is not None and not self.system_prompt.strip():
            self.system_prompt = None


@dataclass
class MCQInput:
    """Input parameters for multiple-choice question solving."""

    question: str
    options: Union[List[str], Dict[str, str]]
    context: Optional[str] = None
    image_paths: Optional[List[str]] = None
