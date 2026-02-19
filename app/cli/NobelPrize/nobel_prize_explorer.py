"""nobel_prize_explorer.py - NobelPrizeWinnerInfo class

Contains the NobelPrizeWinnerInfo class for fetching and managing
Nobel Prize winner information with proper encapsulation.
"""

import os
import re
import logging
from typing import Optional

# Add project root to sys.path to use local 'lite' package
# Use absolute path to ensure correct resolution
import sys
from pathlib import Path

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite import logging_config
from nobel_prize_models import PrizeWinner, PrizeResponse
from nobel_prize_prompts import PromptBuilder


class NobelPrizeWinnerInfo:
    """Explorer class for fetching and managing Nobel Prize winner information."""
    
    def __init__(self, model_config: ModelConfig):
        """
        Initialize Nobel Prize explorer.

        Args:
            model_config: ModelConfig with model settings
        """
        self.model_config = model_config
        self.model = model_config.model or "gemini/gemini-2.5-flash"
        self.client = LiteClient(model_config=model_config)
        self.logger = logging_config.setup_logging(str(Path(__file__).parent / "logs" / "nobel_prize_explorer.log"))
    
    def _validate_model_name(self, model: str) -> None:
        """
        Validate model name format.
        
        Args:
            model: Model name to validate
            
        Raises:
            ValueError: If model name is invalid
        """
        if not re.match(r'^[a-zA-Z0-9\-\./_]+$', model):
            raise ValueError(f"Invalid model name: {model}. Only alphanumeric characters, hyphens, slashes, dots, and underscores are allowed.")
    
    def fetch_winners(self, category: str, year: str, model: Optional[str] = None) -> list[PrizeWinner]:
        """
        Fetch Nobel Prize winners for a specific field and year.

        Args:
            category: Nobel Prize category (Physics, Chemistry, Medicine, Literature, Peace, Economics)
            year: Year of the prize
            model: LLM model to use (defaults to configured model)

        Returns:
            List of PrizeWinner instances

        Raises:
            ValueError: If API response is invalid or model response doesn't match schema
            RuntimeError: If API call fails or required credentials are missing
        """
        if model is None:
            model = self.model
        
        self._validate_model_name(model)

        self.logger.info(f"Fetching Nobel Prize information for {category} in {year} using model: {model}")

        # Create ModelInput with prompt and response format
        model_input = ModelInput(
            user_prompt=PromptBuilder.create_nobel_prize_prompt(category, year),
            response_format=PrizeResponse
        )

        # Generate text using LiteClient (validation handled by client)
        prize_response = self.client.generate_text(model_input=model_input)

        self.logger.info(f"Successfully fetched {len(prize_response.winners)} winner(s)")
        return prize_response.winners
