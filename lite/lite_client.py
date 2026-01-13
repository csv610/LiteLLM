"""Unified LiteClient for text and vision model interactions."""

import argparse
import logging
from typing import Any, Dict, List, Optional, Union

from litellm import completion, APIError
from pydantic import BaseModel

from .config import ModelConfig, ModelInput, DEFAULT_TEMPERATURE
from .image_utils import ImageUtils

logger = logging.getLogger(__name__)

class LiteClient:
    """Unified client for interacting with both text and vision models."""

    @staticmethod
    def _clean_json_response(response_content: str) -> str:
        """
        Clean and repair common JSON issues from LLM responses.

        Args:
            response_content: Raw response from LLM

        Returns:
            Cleaned JSON string

        Raises:
            ValueError: If JSON cannot be repaired
        """
        # Remove non-breaking spaces and other common problematic Unicode characters
        cleaned = response_content.replace('\xa0', ' ').replace('\u200b', '').replace('\ufeff', '')

        # Strip leading/trailing whitespace
        cleaned = cleaned.strip()

        # Try to find and extract JSON object
        if not cleaned.startswith('{'):
            # Try to find the first { and extract from there
            start_idx = cleaned.find('{')
            if start_idx != -1:
                cleaned = cleaned[start_idx:]

        # If JSON doesn't end with }, try to fix it
        if not cleaned.endswith('}'):
            # Find the last } and truncate there
            end_idx = cleaned.rfind('}')
            if end_idx != -1:
                cleaned = cleaned[:end_idx + 1]
            else:
                raise ValueError("Could not find valid JSON structure in response")

        return cleaned

    @staticmethod
    def handle_generation_exception(
        error: Exception,
        is_image_request: bool
    ) -> Union[str, Dict[str, Any]]:
        """
        Handle exceptions from generate_text with appropriate logging and response format.

        Args:
            error: The exception that was raised
            is_image_request: Whether the request involved image analysis

        Returns:
            Error message formatted as string or dict depending on request type
        """
        if isinstance(error, FileNotFoundError):
            error_msg = f"File error: {str(error)}"
        elif isinstance(error, ValueError):
            error_msg = f"Validation Error: {str(error)}"
        elif isinstance(error, APIError):
            error_msg = f"API Error: {str(error)}"
        else:
            error_msg = f"Unexpected error: {str(error)}"

        logger.error(error_msg)

        # Return dict for image requests, string for text-only requests
        return {"error": error_msg} if is_image_request else error_msg

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

        # Handle single image (backward compatibility)
        if model_input.image_path:
            base64_url = ImageUtils.encode_to_base64(model_input.image_path)
            content.append({"type": "image_url", "image_url": {"url": base64_url}})

        # Handle multiple images
        if model_input.image_paths:
            for image_path in model_input.image_paths:
                base64_url = ImageUtils.encode_to_base64(image_path)
                content.append({"type": "image_url", "image_url": {"url": base64_url}})

        messages.append({"role": "user", "content": content})

        return messages

    def generate_text(
        self,
        model_input: ModelInput,
        model_config: Optional[ModelConfig] = None,
    ) -> Union[str, Dict[str, Any], BaseModel]:
        """
        Generate text from a prompt or analyze an image with a prompt.

        Args:
            model_input: ModelInput object containing prompt and image parameters
            model_config: Optional ModelConfig object for model configuration.
                         If not provided, uses the instance's model_config.

        Returns:
            Generated text response (string, parsed Pydantic model, or error dict)
        """
        # Use provided model_config or instance's model_config
        config = model_config or self.model_config
        if not config:
            raise ValueError("ModelConfig must be provided either as argument or during initialization")

        try:
            if model_input.image_path or model_input.image_paths:
                num_images = 1 if model_input.image_path else 0
                num_images += len(model_input.image_paths) if model_input.image_paths else 0
                log_action = f"Analyzing {num_images} image(s)"
            else:
                log_action = "Generating text"
            logger.info(f"{log_action} with model: {config.model}")

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
                cleaned_response = self._clean_json_response(response_content)
                parsed_response = model_input.response_format.model_validate_json(cleaned_response)
                logger.info(f"Successfully parsed response as {model_input.response_format.__name__}")
                return parsed_response

            return response_content

        except Exception as e:
            is_image_request = model_input.image_path is not None or model_input.image_paths is not None
            return self.handle_generation_exception(e, is_image_request)

def main():
    """Main entry point for the LiteClient CLI."""
    parser = argparse.ArgumentParser(
        description="Unified LiteClient for text and vision model interactions"
    )

    parser.add_argument(
        "-i",
        "--image_path",
        type=str,
        default=None,
        help="Path to the image file (if provided, vision analysis is used)",
    )
    parser.add_argument(
        "-q",
        "--question",
        type=str,
        help="The input prompt for the model or image analysis",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="perplexity/sonar",
        help="The model identifier (auto-selected if not provided)",
    )
    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help=f"Sampling temperature (default: {DEFAULT_TEMPERATURE})",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Initialize client with ModelConfig
    model_config = ModelConfig(model=args.model, temperature=args.temperature)

    client = LiteClient(model_config=model_config)

    # Create ModelInput
    model_input = ModelInput(
        user_prompt=args.question,
        image_path=args.image_path
    )

    # Single unified generate_text call
    result = client.generate_text(model_input=model_input)

    print(result)


if __name__ == "__main__":
    main()
