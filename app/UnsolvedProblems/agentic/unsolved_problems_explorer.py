"""
unsolved_problems_explorer.py - Explorer class for unsolved problems

Contains the UnsolvedProblemsExplorer class for fetching and managing
unsolved problems in various academic fields.
"""

import logging
from typing import List, Optional

from lite import LiteClient, ModelConfig
from lite.config import ModelInput

from unsolved_problems_models import (
    ReviewedUnsolvedProblemsResponse,
    UnsolvedProblem,
    UnsolvedProblemsResponse,
)
from unsolved_problems_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class UnsolvedProblemsExplorer:
    """Explorer class for fetching and managing unsolved problems."""

    def __init__(self, model_config: ModelConfig):
        """Initialize explorer with model configuration.

        Args:
            model_config: ModelConfig instance with model and temperature settings
        """
        self.model_config = model_config
        self.model = model_config.model
        self.temperature = model_config.temperature
        self.client = LiteClient(model_config=self.model_config)

    def generate_text(self, topic: str, num_problems: int) -> List[UnsolvedProblem]:
        """Fetch unsolved problems using a 2-agent generation and review flow.

        Args:
            topic: The topic to find unsolved problems for
            num_problems: Number of unsolved problems to retrieve

        Returns:
            List of UnsolvedProblem instances

        Raises:
            RuntimeError: If either agent returns an invalid response
        """
        logger.info(
            "Fetching %s unsolved problems in %s using model: %s",
            num_problems,
            topic,
            self.model_config.model,
        )

        draft_response = self._run_research_agent(topic, num_problems)
        reviewed_response = self._run_review_agent(topic, num_problems, draft_response)
        return reviewed_response.problems

    def _run_research_agent(
        self, topic: str, num_problems: int
    ) -> UnsolvedProblemsResponse:
        """Run the first pass that drafts candidate problems."""
        model_input = ModelInput(
            system_prompt=PromptBuilder.get_generation_system_prompt(),
            user_prompt=PromptBuilder.get_generation_user_prompt(topic, num_problems),
            response_format=UnsolvedProblemsResponse,
        )
        response = self.client.generate_text(model_input)
        if isinstance(response, str):
            raise RuntimeError(f"Research agent failed: {response}")
        return response

    def _run_review_agent(
        self,
        topic: str,
        num_problems: int,
        draft_response: UnsolvedProblemsResponse,
    ) -> ReviewedUnsolvedProblemsResponse:
        """Run the second pass that validates and normalizes the draft."""
        model_input = ModelInput(
            system_prompt=PromptBuilder.get_review_system_prompt(),
            user_prompt=PromptBuilder.get_review_user_prompt(
                topic=topic,
                num_problems=num_problems,
                draft_payload=draft_response.model_dump(),
            ),
            response_format=ReviewedUnsolvedProblemsResponse,
        )
        response = self.client.generate_text(model_input)
        if isinstance(response, str):
            raise RuntimeError(f"Review agent failed: {response}")
        return response

    def update_model(self, model: str, temperature: Optional[float] = None) -> None:
        """Update the model configuration.

        Args:
            model: New model name to use
            temperature: New temperature setting (optional)
        """
        self.model = model

        if temperature is not None:
            self.temperature = temperature

        self.model_config = ModelConfig(model=self.model, temperature=self.temperature)
        self.client = LiteClient(model_config=self.model_config)

    def get_model_info(self) -> dict:
        """Get information about the current model configuration.

        Returns:
            dict: Dictionary containing model information
        """
        return {
            "model": self.model,
            "temperature": self.temperature
        }
