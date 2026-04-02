"""Unified LiteClient for text and vision model interactions."""

import logging
from typing import Any, Dict, List, Optional, Union

from litellm import APIError, completion
from pydantic import BaseModel
from .utils.json_cleaner import JSONCleaner

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
        retries: int = 2,
    ) -> Union[str, BaseModel, Dict[str, Any]]:
        """
        Generate text from a prompt or analyze an image with a prompt.

        Args:
            model_input: ModelInput object containing prompt and image parameters
            model_config: Optional ModelConfig object for model configuration.
            retries: Number of retries for the model call.

        Returns:
            Generated text response (string, parsed Pydantic model, or error dict)
        """
        # Use provided model_config or instance
        config = model_config or self.model_config
        if not config:
            raise ValueError("ModelConfig must be provided")

        last_exception = None
        for attempt in range(retries + 1):
            try:
                logger.info(
                    f"Generating completion (attempt {attempt + 1}) with model: {config.model}"
                )
                messages = self.create_message(model_input)

                response = completion(
                    model=config.model,
                    messages=messages,
                    temperature=config.temperature,
                    response_format=model_input.response_format,
                )

                response_content = response.choices[0].message.content

                if (
                    model_input.response_format
                    and isinstance(model_input.response_format, type)
                    and issubclass(model_input.response_format, BaseModel)
                ):
                    try:
                        cleaned_json = JSONCleaner.extract_json(response_content)
                        # DEBUG: Log what we're trying to parse
                        print(
                            f"DEBUG: Attempting to parse JSON: '{cleaned_json[:200]}...'"
                        )
                        parsed_response = (
                            model_input.response_format.model_validate_json(
                                cleaned_json
                            )
                        )
                        logger.info(
                            f"Successfully parsed response as {model_input.response_format.__name__}"
                        )
                        return parsed_response
                    except Exception as e:
                        logger.warning(
                            "Failed to parse response as %s; returning raw content",
                            model_input.response_format.__name__,
                        )
                        # DEBUG: Log the error and raw content
                        print(f"DEBUG: JSON parsing failed: {e}")
                        print(
                            f"DEBUG: Raw response content: '{response_content[:500]}...'"
                        )
                        return response_content

                return response_content
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                last_exception = e
                continue
        has_image = bool(model_input.image_path or model_input.image_paths)
        if isinstance(last_exception, FileNotFoundError):
            message = f"File error: {last_exception}"
            return {"error": message} if has_image else message
        if isinstance(last_exception, ValueError):
            message = str(last_exception)
            return {"error": message} if has_image else message
        if isinstance(last_exception, APIError):
            message = f"API Error: {last_exception}"
            return {"error": message} if has_image else message
        if last_exception is not None:
            message = str(last_exception)
            return {"error": message} if has_image else message
        return {"error": "Unknown error"} if has_image else "Unknown error"
