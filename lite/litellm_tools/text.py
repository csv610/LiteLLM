"""LiteText module for language model interactions."""

import logging
import time
from dataclasses import dataclass
from typing import Optional

from logging_config import configure_logging

logger = logging.getLogger(__name__)

from litellm import completion, APIError

class LiteText:
    """Main class for interacting with the LiteText API."""

    DEFAULT_TEMPERATURE = 0.2
    DEFAULT_MAX_TOKENS = 1000

    def generate_text(
        self, 
        prompt: str,
        model: str,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> str:
        """
        Send a prompt to the specified model and return the response with metrics.

        Args:
            prompt: The input prompt for the model
            model: The model identifier (e.g., "openai/gpt-4o")
            temperature: Sampling temperature (default: 0.2)
            max_tokens: Maximum tokens in response (default: 1000)
        """
        if not prompt or not prompt.strip():
            return "Error: Prompt cannot be empty"

        try:
            response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            response_text = response.choices[0].message.content
            return response_text

        except APIError as e:
            error_msg = f"API Error: {str(e)}"
            logger.error(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return error_msg


import argparse
def main():
    """Main entry point for the LiteText CLI."""
    parser = argparse.ArgumentParser(
        description="Generate text using language models via LiteText"
    )
    parser.add_argument(
        "-q", "--question",
        type=str,
        help="The input prompt for the model"
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        default="perplexity/sonar",
        help="The model identifier (default: perplexity/sonar)"
    )
    parser.add_argument(
        "-t", "--temperature",
        type=float,
        default=LiteText.DEFAULT_TEMPERATURE,
        help=f"Sampling temperature (default: {LiteText.DEFAULT_TEMPERATURE})"
    )
    parser.add_argument(
        "-tk", "--max-tokens",
        type=int,
        default=LiteText.DEFAULT_MAX_TOKENS,
        help=f"Maximum tokens in response (default: {LiteText.DEFAULT_MAX_TOKENS})"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Configure logging to file only
    log_level = logging.DEBUG if args.verbose else logging.INFO
    configure_logging(log_file="litetext.log", level=log_level)

    lite_text = LiteText()

    response = lite_text.generate_text(
        prompt=args.question,
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )

    print(response)


if __name__ == "__main__":
    main()
