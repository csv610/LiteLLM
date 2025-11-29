"""LiteVision module for image analysis using language models."""

import base64
import logging
import time
from typing import Dict, Optional

from litellm import completion

logger = logging.getLogger(__name__)


class LiteVision:
    """Main class for interacting with vision models for image analysis."""

    DEFAULT_TEMPERATURE = 0.2
    DEFAULT_MAX_TOKENS = 1000

    @staticmethod
    def image_to_base64(image_path: str) -> Optional[str]:
        """
        Convert an image file to base64 encoding.

        Args:
            image_path: Path to the image file

        Returns:
            Base64 encoded image URL, or None if file not found

        Raises:
            FileNotFoundError: If the image file doesn't exist
        """
        try:
            with open(image_path, "rb") as file:
                file_data = file.read()
                encoded_file = base64.b64encode(file_data).decode("utf-8")
                base64_url = f"data:image/jpeg;base64,{encoded_file}"
            return base64_url
        except FileNotFoundError:
            logger.error(f"Image file not found: {image_path}")
            raise

    @staticmethod
    def get_response(
        prompt: str,
        image_file: str,
        model: str,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> Dict[str, any]:
        """
        Analyze an image with a given prompt using the specified model.

        Args:
            prompt: The prompt to analyze the image
            image_file: Path to the image file
            model: The model identifier (e.g., "openai/gpt-4o")
            temperature: Sampling temperature (default: 0.2)
            max_tokens: Maximum tokens in response (default: 1000)

        Returns:
            Dictionary containing 'text', 'response_time', 'word_count', or 'error'
        """
        try:
            start_time = time.time()
            logger.info(f"Analyzing image with model: {model}")

            base64_url = LiteVision.image_to_base64(image_file)
            image_content = [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": base64_url}},
            ]

            response = completion(
                model=model,
                messages=[{"role": "user", "content": image_content}],
                temperature=temperature,
                max_tokens=max_tokens,
            )

            response_time = time.time() - start_time
            response_text = response.choices[0].message.content
            word_count = len(response_text.split())

            logger.info(f"Image analysis completed in {response_time:.2f} seconds")
            return {
                "text": response_text,
                "response_time": response_time,
                "word_count": word_count,
            }
        except FileNotFoundError as e:
            error_msg = f"File not found: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg, "response_time": 0, "word_count": 0}
        except Exception as e:
            error_msg = f"Error analyzing image: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg, "response_time": 0, "word_count": 0}
