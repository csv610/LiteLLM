"""nobel_prize_explorer.py - NobelPrizeWinnerInfo class

Contains the NobelPrizeWinnerInfo class for fetching and managing
Nobel Prize winner information with proper encapsulation.
"""

import re

# Add project root to sys.path to use local 'lite' package
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite import logging_config
from .nobel_prize_models import PrizeWinner, PrizeResponse
from .nobel_prize_prompts import PromptBuilder


class NobelPrizeWinnerInfo:
    """Explorer class for fetching and managing Nobel Prize winner information."""
    
    def __init__(self, model_config: ModelConfig):
        """
        Initialize Nobel Prize explorer.

        Args:
            model_config: ModelConfig with model settings
        """
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.logger = logging_config.configure_logging(str(Path(__file__).parent / "logs" / "nobel_prize_explorer.log"))

    def _run_agent(
        self,
        *,
        agent_name: str,
        prompt: str,
        model_config: ModelConfig,
    ) -> PrizeResponse:
        """Run a single structured agent pass and validate its response."""
        self.logger.info(f"Running {agent_name} with model: {model_config.model}")

        model_input = ModelInput(
            system_prompt=PromptBuilder.create_agent_system_prompt(agent_name),
            user_prompt=prompt,
            response_format=PrizeResponse
        )
        agent_response = self.client.generate_text(
            model_input=model_input,
            model_config=model_config,
        )
        if not isinstance(agent_response, PrizeResponse):
            raise RuntimeError(f"{agent_name} returned invalid response: {agent_response}")
        return agent_response
    
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
    
    def fetch_winners(self, category: str, year: str, model: str) -> list[PrizeWinner]:
        """
        Fetch Nobel Prize winners for a specific field and year.

        Args:
            category: Nobel Prize category (Physics, Chemistry, Medicine, Literature, Peace, Economics)
            year: Year of the prize
            model: LLM model to use for both agents

        Returns:
            List of PrizeWinner instances

        Raises:
            ValueError: If API response is invalid or model response doesn't match schema
            RuntimeError: If API call fails or required credentials are missing
        """
        self._validate_model_name(model)

        self.logger.info(
            f"Fetching Nobel Prize information for {category} in {year} using two-agent workflow with model: {model}"
        )

        generation_config = ModelConfig(model=model, temperature=self.model_config.temperature)
        validation_config = ModelConfig(model=model, temperature=0.0)

        generated_response = self._run_agent(
            agent_name="generation_agent",
            prompt=PromptBuilder.create_nobel_prize_prompt(category, year),
            model_config=generation_config,
        )
        self.logger.info(f"Generation agent produced {len(generated_response.winners)} winner(s)")

        validated_response = self._run_agent(
            agent_name="validation_agent",
            prompt=PromptBuilder.create_validation_prompt(category, year, generated_response),
            model_config=validation_config,
        )
        self.logger.info(f"Validation agent approved {len(validated_response.winners)} winner(s)")

        return validated_response.winners
