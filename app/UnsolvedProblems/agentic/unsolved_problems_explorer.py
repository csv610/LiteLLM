"""
unsolved_problems_explorer.py - Explorer class for unsolved problems

Contains the UnsolvedProblemsExplorer class for fetching and managing
unsolved problems in various academic fields using a 3-tier artifact approach.
"""

import logging
import json
from typing import List, Optional

from lite import LiteClient, ModelConfig
from lite.config import ModelInput

from app.UnsolvedProblems.shared.models import (
    ReviewedUnsolvedProblemsResponse,
    UnsolvedProblem,
    UnsolvedProblemsResponse,
    ModelOutput
)
from app.UnsolvedProblems.shared.prompts import PromptBuilder

logger = logging.getLogger(__name__)


class UnsolvedProblemsExplorer:
    """Explorer class for fetching and managing unsolved problems."""

    def __init__(self, model_config: ModelConfig):
        """Initialize explorer with model configuration."""
        self.model_config = model_config
        self.model = model_config.model
        self.temperature = model_config.temperature
        self.client = LiteClient(model_config=self.model_config)

    def generate_text(self, topic: str, num_problems: int) -> ModelOutput:
        """Fetch unsolved problems using a 3-tier multi-agent approach."""
        logger.info(
            "Fetching 3-tier unsolved problems in %s using model: %s",
            topic,
            self.model_config.model,
        )

        # Tier 1: Specialist Research (JSON)
        draft_response = self._run_research_agent(topic, num_problems)
        
        # Tier 2: Auditor Stage (JSON Review)
        reviewed_response = self._run_review_agent(topic, num_problems, draft_response)

        # Tier 3: Output Synthesis (Markdown Closer)
        logger.debug("Synthesizing final Markdown report...")
        synth_prompt = (
            f"Synthesize a beautiful Markdown investigation report for unsolved problems in: '{topic}'.\n\n"
            f"IDENTIFIED PROBLEMS:\n"
            + "\n".join([f"- {p.name}: {p.description}" for p in reviewed_response.problems])
        )
        
        final_markdown_res = self.client.generate_text(ModelInput(
            system_prompt="You are a Lead Academic Editor. Synthesize a list of unsolved problems into a professional Markdown report with history and significance sections.",
            user_prompt=synth_prompt,
            response_format=None
        ))
        final_markdown = final_markdown_res.markdown

        return ModelOutput(
            data=draft_response,
            markdown=final_markdown,
            metadata={
                "reviewed_payload": reviewed_response.model_dump() if hasattr(reviewed_response, 'model_dump') else {},
                "reviewer_notes": reviewed_response.reviewer_notes
            }
        )

    def _run_research_agent(
        self, topic: str, num_problems: int
    ) -> UnsolvedProblemsResponse:
        """Run the first pass that drafts candidate problems (Tier 1 Specialist)."""
        model_input = ModelInput(
            system_prompt=PromptBuilder.get_generation_system_prompt(),
            user_prompt=PromptBuilder.get_generation_user_prompt(topic, num_problems),
            response_format=UnsolvedProblemsResponse,
        )
        response_res = self.client.generate_text(model_input)
        return response_res.data

    def _run_review_agent(
        self,
        topic: str,
        num_problems: int,
        draft_response: UnsolvedProblemsResponse,
    ) -> ReviewedUnsolvedProblemsResponse:
        """Run the second pass that validates and normalizes (Tier 2 Auditor)."""
        model_input = ModelInput(
            system_prompt=PromptBuilder.get_review_system_prompt(),
            user_prompt=PromptBuilder.get_review_user_prompt(
                topic=topic,
                num_problems=num_problems,
                draft_payload=draft_response.model_dump(),
            ),
            response_format=ReviewedUnsolvedProblemsResponse,
        )
        response_res = self.client.generate_text(model_input)
        return response_res.data

    def update_model(self, model: str, temperature: Optional[float] = None) -> None:
        """Update the model configuration."""
        self.model = model
        if temperature is not None:
            self.temperature = temperature
        self.model_config = ModelConfig(model=self.model, temperature=self.temperature)
        self.client = LiteClient(model_config=self.model_config)

    def get_model_info(self) -> dict:
        """Get information about the current model configuration."""
        return {
            "model": self.model,
            "temperature": self.temperature
        }
