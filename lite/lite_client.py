"""Unified LiteClient for text and vision model interactions."""

import logging
from typing import Any, Dict, List, Optional, Union

from litellm import completion
from pydantic import BaseModel

from .config import ModelConfig, ModelInput
from .image_utils import ImageUtils

logger = logging.getLogger(__name__)

class LiteClient:
    """Unified client for interacting with both text and vision models."""

    def __init__(self, model_config: Optional[ModelConfig] = None):
        """
        Initialize LiteClient with optional ModelConfig.

        Args:
            model_config: Optional ModelConfig instance for model configuration.
        """
        self.model_config = model_config

    @staticmethod
    def create_message(model_input: ModelInput) -> List[Dict[str, Any]]:
        """
        Create a message for the model.

        Args:
            model_input: ModelInput object containing prompt and image parameters

        Returns:
            Message list formatted for the completion API
        """
        messages = []

        # Add system message if provided
        if model_input.system_prompt:
            messages.append({"role": "system", "content": model_input.system_prompt})

        content = [{"type": "text", "text": model_input.user_prompt}]

        # Handle images (single and multiple)
        all_image_paths = []
        if model_input.image_path:
            all_image_paths.append(model_input.image_path)
        if model_input.image_paths:
            all_image_paths.extend(model_input.image_paths)

        for image_path in all_image_paths:
            base64_url = ImageUtils.encode_to_base64(image_path)
            content.append({"type": "image_url", "image_url": {"url": base64_url}})

        messages.append({"role": "user", "content": content})

        return messages

    def generate_text(
        self,
        model_input: ModelInput,
        model_config: Optional[ModelConfig] = None,
    ) -> Union[str, BaseModel]:
        """
        Generate text from a prompt or analyze an image with a prompt.

        Args:
            model_input: ModelInput object containing prompt and image parameters
            model_config: Optional ModelConfig object for model configuration.
                         If not provided, uses the instance's model_config.

        Returns:
            Generated text response (string or parsed Pydantic model)
        """
        # Use provided model_config or instance's model_config
        config = model_config or self.model_config
        if not config:
            raise ValueError("ModelConfig must be provided either as argument or during initialization")

        logger.info(f"Generating completion with model: {config.model}")

        # Create message and call completion
        messages = self.create_message(model_input)

        response = completion(
            model=config.model,
            messages=messages,
            temperature=config.temperature,
            response_format=model_input.response_format,
        )

        logger.info("Request successful")
        response_content = response.choices[0].message.content

        # If response_format is a Pydantic model, parse and validate the response
        if model_input.response_format and isinstance(model_input.response_format, type) and issubclass(model_input.response_format, BaseModel):
            parsed_response = model_input.response_format.model_validate_json(response_content)
            logger.info(f"Successfully parsed response as {model_input.response_format.__name__}")
            return parsed_response

        return response_content

