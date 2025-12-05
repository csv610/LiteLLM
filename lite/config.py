"""Configuration for available models and vision processing parameters."""

from dataclasses import dataclass
from typing import Optional

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
    system_prompt: Optional[str] = None
    response_format: Optional[str] = None

    def __post_init__(self):
        """Validate input after initialization."""
        if not self.user_prompt or not self.user_prompt.strip():
            if not self.image_path:
                raise ValueError("user_prompt cannot be empty unless an image_path is provided")
            self.user_prompt = DEFAULT_PROMPT

        # Normalize empty system_prompt to None
        if self.system_prompt is not None and not self.system_prompt.strip():
            self.system_prompt = None

        # Normalize empty response_format to None
        if self.response_format is not None and isinstance(self.response_format, str) and not self.response_format.strip():
            self.response_format = None
