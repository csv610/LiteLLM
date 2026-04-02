"""nobel_prize_explorer.py - NobelPrizeWinnerInfo class with 3-tier artifact output"""

import re
import logging
import sys
from pathlib import Path
from typing import Optional, List, Any, Dict

# Add project root to sys.path to use local 'lite' package
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite import logging_config
from app.NobelPrizeWinners.shared.models import PrizeWinner, PrizeResponse, ModelOutput
from app.NobelPrizeWinners.shared.prompts import PromptBuilder


class NobelPrizeWinnerInfo:
    """Explorer class for fetching and managing Nobel Prize winner information using a 3-tier approach."""
    
    def __init__(self, model_config: ModelConfig):
        """Initialize Nobel Prize explorer."""
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
        """Run a single structured agent pass (Tier 1/2 Specialist/Auditor)."""
        self.logger.info(f"Running {agent_name} with model: {model_config.model}")

        model_input = ModelInput(
            system_prompt=PromptBuilder.create_agent_system_prompt(agent_name),
            user_prompt=prompt,
            response_format=PrizeResponse
        )
        res = self.client.generate_text(
            model_input=model_input,
            model_config=model_config,
        )
        return res.data
    
    def fetch_winners(self, category: str, year: str, model: str) -> ModelOutput:
        """Fetch Nobel Prize winners using a 3-tier multi-agent approach."""
        if not re.match(r'^[a-zA-Z0-9\-\./_]+$', model):
            raise ValueError(f"Invalid model name: {model}")

        self.logger.info(f"Fetching 3-tier Nobel Prize info for {category} ({year})")

        # Tier 1: Generation Specialist (JSON)
        generation_config = ModelConfig(model=model, temperature=self.model_config.temperature)
        generated_response = self._run_agent(
            agent_name="generation_agent",
            prompt=PromptBuilder.create_nobel_prize_prompt(category, year),
            model_config=generation_config,
        )

        # Tier 2: Validation Auditor (JSON)
        validation_config = ModelConfig(model=model, temperature=0.0)
        validated_response = self._run_agent(
            agent_name="validation_agent",
            prompt=PromptBuilder.create_validation_prompt(category, year, generated_response),
            model_config=validation_config,
        )

        # Tier 3: Output Synthesis (Markdown Closer)
        logger.debug("Synthesizing final Markdown report...")
        winners_json = validated_response.model_dump_json(indent=2)
        synth_prompt = (
            f"Synthesize a beautiful, celebratory Markdown report for the Nobel Prize in {category} for the year {year}.\n\n"
            f"WINNERS DATA:\n{winners_json}"
        )
        
        final_markdown_res = self.client.generate_text(ModelInput(
            system_prompt="You are a Lead Science Historian and Editor. Synthesize prize winner data into a professional Markdown report with biography and impact sections.",
            user_prompt=synth_prompt,
            response_format=None
        ))
        final_markdown = final_markdown_res.markdown

        return ModelOutput(
            data=validated_response,
            markdown=final_markdown,
            metadata={
                "category": category,
                "year": year,
                "winner_count": len(validated_response.winners)
            }
        )
