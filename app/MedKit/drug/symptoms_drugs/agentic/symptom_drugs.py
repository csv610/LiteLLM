#!/usr/bin/env python3
"""
Symptom-to-Drug Analysis module.

This module provides the core SymptomDrugs class for listing medications
prescribed for specific symptoms based on clinical guidance.
"""

import logging
from pathlib import Path

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response
from symptom_drugs_models import ModelOutput, SymptomDrugAnalysisModel
from symptom_drugs_prompts import PromptBuilder, SymptomInput

logger = logging.getLogger(__name__)


class SymptomDrugs:
    """Analyzes symptoms to list medications typically used for treatment."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.config = None  # Store the configuration for later use in save
        logger.debug("Initialized SymptomDrugs")

    def generate_text(
        self, config: SymptomInput, structured: bool = False
    ) -> ModelOutput:
        """
        Analyzes symptoms and lists potential medications for treatment using 3 agents.

        Args:
            config: Configuration and input for analysis
            structured: Whether to use structured output

        Returns:
            ModelOutput: The analysis result
        """
        # Store the configuration for later use in save
        self.config = config
        logger.info(f"Starting 3-agent analysis for: {config.symptom_name}")

        # 1. Researcher Agent
        logger.info("-> Researcher: Identifying medications...")
        researcher_input = ModelInput(
            system_prompt=PromptBuilder.create_researcher_system_prompt(),
            user_prompt=PromptBuilder.create_researcher_user_prompt(config),
        )
        researcher_result = self._ask_llm(researcher_input)
        researcher_output = researcher_result.markdown

        # 2. Safety Agent
        logger.info("-> Safety Specialist: Analyzing risks and red flags...")
        safety_input = ModelInput(
            system_prompt=PromptBuilder.create_safety_system_prompt(),
            user_prompt=PromptBuilder.create_safety_user_prompt(config),
        )
        safety_result = self._ask_llm(safety_input)
        safety_output = safety_result.markdown

        # 3. Reviewer Agent
        logger.info("-> Reviewer: Synthesizing final report...")
        response_format = None
        if structured:
            response_format = SymptomDrugAnalysisModel

        reviewer_input = ModelInput(
            system_prompt=PromptBuilder.create_reviewer_system_prompt(),
            user_prompt=PromptBuilder.create_reviewer_user_prompt(
                config, researcher_output, safety_output
            ),
            response_format=response_format,
        )
        final_result = self._ask_llm(reviewer_input)

        logger.info(f"✓ Successfully completed 3-agent analysis for: {config.symptom_name}")
        return final_result

    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Helper to call LiteClient with error handling and ensure ModelOutput return."""
        logger.debug("Calling LiteClient...")
        try:
            response = self.client.generate_text(model_input=model_input)
            
            # If the response is already a ModelOutput, return it
            if isinstance(response, ModelOutput):
                return response
            
            # If it's a Pydantic model (structured output from LiteClient)
            if hasattr(response, "model_dump"):
                return ModelOutput(data=response)
                
            # If it's a string, wrap it in ModelOutput as markdown
            if isinstance(response, str):
                return ModelOutput(markdown=response)
            
            # Fallback for other types
            return ModelOutput(markdown=str(response))
            
        except Exception as e:
            logger.error(f"✗ Error during LLM analysis: {e}")
            logger.exception("Full exception details:")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the symptom-to-drug analysis to a file."""
        if self.config is None:
            raise ValueError(
                "No configuration information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        symptom_safe = self.config.symptom_name.lower().replace(" ", "_")
        base_filename = f"{symptom_safe}_drug_recommendations"

        return save_model_response(result, output_dir / base_filename)
