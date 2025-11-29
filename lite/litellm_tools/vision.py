"""LiteVision module for image analysis using language models."""

import logging
import time
from typing import Any, Dict

from litellm import completion

from image_utils import ImageUtils
from response_processor import ResponseProcessor

logger = logging.getLogger(__name__)


class LiteVision:
    """Main class for interacting with vision models for image analysis."""

    def generate_text(
        self,
        image_path: str,
        prompt: str,
        model: str,
        temperature: float = 0.2,
        max_tokens: int = 2000,
    ) -> Dict[str, Any]:
        """
        Generate text from an image with a given prompt using the specified model.

        Args:
            image_path: Path to the image file
            prompt: The prompt to analyze the image
            model: The model identifier (e.g., "openai/gpt-4o")
            temperature: Sampling temperature (default: 0.2)
            max_tokens: Maximum tokens in response (default: 2000)

        Returns:
            Dictionary containing analysis result or error
        """
        try:
            logger.info(f"Analyzing image with model: {model}")

            # Encode image
            base64_url = ImageUtils.encode_to_base64(image_path)

            # Build message
            image_content = [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": base64_url}},
            ]

            # Call API
            response = completion(
                model=model,
                messages=[{"role": "user", "content": image_content}],
                temperature=temperature,
                max_tokens=max_tokens,
            )

            # Extract and format response
            response_text = ResponseProcessor.extract_text(response)
            if not response_text:
                return ResponseProcessor.format_error("No response text received")

            return response_text

        except FileNotFoundError as e:
            error_msg = f"File not found: {str(e)}"
            logger.error(error_msg)
            return ResponseProcessor.format_error(error_msg)
        except Exception as e:
            error_msg = f"Error analyzing image: {str(e)}"
            logger.error(error_msg)
            return ResponseProcessor.format_error(error_msg)


def main():
    """Main function to demonstrate LiteVision usage."""
    from cli import VisionCLI

    args = VisionCLI.parse_arguments()

    client = LiteVision()

    result = client.generate_text(
        image_path=args.image_path,
        prompt=args.prompt,
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )

    print(result)


if __name__ == "__main__":
    main()
