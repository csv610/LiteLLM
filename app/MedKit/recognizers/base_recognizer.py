from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Type, Union

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from pydantic import BaseModel

from .models import ModelOutput

if TYPE_CHECKING:
    from .models import ModelOutput


class BaseRecognizer(ABC):
    """Base class for all medical entity recognizers."""

    def __init__(self, model_config: ModelConfig):
        """
        Initialize the recognizer with model configuration.

        Args:
            model_config: Configuration for the model (model name, temperature, etc.)
        """
        self.model_config = model_config
        self.client = LiteClient(model_config)

    @abstractmethod
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        """
        Identify a medical entity by name.

        Args:
            name: The name of the entity to identify.
            structured: Whether to return a structured Pydantic model or raw text.

        Returns:
            The identification result as ModelOutput.
        """
        pass

    def _generate(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: Optional[Type[BaseModel]] = None,
    ) -> Union[str, BaseModel]:
        """
        Helper method to generate text using the LiteClient.

        Args:
            system_prompt: The system prompt to use.
            user_prompt: The user prompt to use.
            response_format: Optional Pydantic model for structured output.

        Returns:
            The generated response.
        """
        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )
        return self.client.generate_text(model_input=model_input)
