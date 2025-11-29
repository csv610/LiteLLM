"""LiteText module for language model interactions."""

import logging
import time
from dataclasses import dataclass
from typing import Optional

from litellm import completion, APIError

logger = logging.getLogger(__name__)


@dataclass
class LiteTextResponse:
    """Encapsulates response data from LiteText API."""

    response: Optional[str] = None
    response_time: float = 0.0
    word_count: int = 0
    error: Optional[str] = None

    def is_success(self) -> bool:
        """Check if the request was successful."""
        return self.error is None


class LiteText:
    """Main class for interacting with the LiteText API."""

    DEFAULT_TEMPERATURE = 0.2
    DEFAULT_MAX_TOKENS = 1000

    @staticmethod
    def get_response(
        prompt: str,
        model: str,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> LiteTextResponse:
        """
        Send a prompt to the specified model and return the response with metrics.

        Args:
            prompt: The input prompt for the model
            model: The model identifier (e.g., "openai/gpt-4o")
            temperature: Sampling temperature (default: 0.2)
            max_tokens: Maximum tokens in response (default: 1000)

        Returns:
            LiteTextResponse object containing response text, timing, and word count
        """
        if not prompt or not prompt.strip():
            return LiteTextResponse(error="Prompt cannot be empty")

        try:
            logger.info(f"Sending request to model: {model}")
            start_time = time.time()

            response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )

            response_time = time.time() - start_time
            response_text = response.choices[0].message.content
            word_count = len(response_text.split())

            logger.info(f"Response received in {response_time:.2f} seconds")
            return LiteTextResponse(
                response=response_text,
                response_time=response_time,
                word_count=word_count,
            )
        except APIError as e:
            error_msg = f"API Error: {str(e)}"
            logger.error(error_msg)
            return LiteTextResponse(error=error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return LiteTextResponse(error=error_msg)
