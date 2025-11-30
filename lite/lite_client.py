"""Unified LiteClient for text and vision model interactions."""

import argparse
import logging
from typing import Any, Dict, Optional, Union

from litellm import completion, APIError

from config import ModelConfig
from image_utils import ImageUtils

logger = logging.getLogger(__name__)


class LiteClient:
    """Unified client for interacting with both text and vision models."""

    DEFAULT_TEMPERATURE = 0.2

    @staticmethod
    def create_message(prompt: str, image_path: Optional[str] = None) -> list:
        """
        Create a message for the model.

        Args:
            prompt: The input prompt for the model
            image_path: Optional path to image file for vision analysis

        Returns:
            Message list formatted for the completion API
        """

        content = [{"type": "text", "text": prompt}]

        if image_path:
            base64_url = ImageUtils.encode_to_base64(image_path)
            content.append({"type": "image_url", "image_url": {"url": base64_url}})

        return [{"role": "user", "content": content}]

    def generate_text(
        self,
        prompt: str,
        model: str,
        image_path: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
    ) -> Union[str, Dict[str, Any]]:
        """
        Generate text from a prompt or analyze an image with a prompt.

        Args:
            prompt: The input prompt for the model or image analysis
            model: The model identifier (e.g., "openai/gpt-4o")
            temperature: Sampling temperature (default: 0.2)
            image_path: Optional path to image file for vision analysis

        Returns:
            Generated text response or error message
        """
        if not prompt or not prompt.strip():
            if image_path:
                prompt = "Describe the image"
            else:
                return "Error: Prompt cannot be empty"

        try:
            log_action = "Analyzing image" if image_path else "Generating text"
            logger.info(f"{log_action} with model: {model}")

            # Create message and call completion
            messages = self.create_message(prompt, image_path)
            response = completion(
                model=model,
                messages=messages,
                temperature=temperature,
            )

            logger.info("Request successful")
            return response.choices[0].message.content

        except FileNotFoundError as e:
            error_msg = f"File error: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg} if image_path else error_msg
        except ValueError as e:
            error_msg = f"Validation Error: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg} if image_path else error_msg
        except APIError as e:
            error_msg = f"API Error: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg} if image_path else error_msg
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg} if image_path else error_msg

    @staticmethod
    def list_models(model_type: str = "text") -> list:
        """Get list of available models by type."""
        return ModelConfig.get_models(model_type=model_type)

    @staticmethod
    def get_model(index: int, model_type: str = "text") -> Optional[str]:
        """Get model by index and type."""
        return ModelConfig.get_model(index, model_type=model_type)


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
        default=LiteClient.DEFAULT_TEMPERATURE,
        help=f"Sampling temperature (default: {LiteClient.DEFAULT_TEMPERATURE})",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Initialize client
    client = LiteClient()

    # Single unified generate_text call
    result = client.generate_text(
        prompt=args.question,
        image_path=args.image_path,
        model=args.model,
        temperature=args.temperature
    )

    print(result)


if __name__ == "__main__":
    main()
