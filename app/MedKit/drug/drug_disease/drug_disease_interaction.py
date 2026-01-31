#!/usr/bin/env python3
"""
Drug-Disease Interaction Analysis module.

This module provides the core DrugDiseaseInteraction class for analyzing
how medical conditions affect drug efficacy, safety, and metabolism.
"""

import logging
from pathlib import Path
from typing import Optional, Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from drug_disease_interaction_models import DrugDiseaseInteractionModel, ModelOutput
from drug_disease_interaction_prompts import PromptBuilder, DrugDiseaseInput, PromptStyle

logger = logging.getLogger(__name__)


class DrugDiseaseInteraction:
    """Analyzes drug-disease interactions based on provided configuration."""
    
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.config = None  # Store the configuration for later use in save
        logger.debug(f"Initialized DrugDiseaseInteraction")

    def generate_text(self, config: DrugDiseaseInput, structured: bool = False) -> ModelOutput:
        """
        Analyzes how a medical condition affects drug efficacy, safety, and metabolism.

        Args:
            config: Configuration and input for analysis
            structured: Whether to use structured output

        Returns:
            ModelOutput: The analysis result
        """
        # Store the configuration for later use in save
        self.config = config
        logger.debug(f"Starting drug-disease interaction analysis")
        logger.debug(f"Medicine: {config.medicine_name}")
        logger.debug(f"Condition: {config.condition_name}")

        user_prompt = PromptBuilder.create_user_prompt(config)
        response_format = None
        if structured:
            response_format = DrugDiseaseInteractionModel

        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=user_prompt,
            response_format=response_format,
        )
        result = self._ask_llm(model_input)
        
        logger.debug(f"✓ Successfully analyzed disease interaction")
        return result

    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Helper to call LiteClient with error handling."""
        logger.debug("Calling LiteClient...")
        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"✗ Error during LLM analysis: {e}")
            logger.exception("Full exception details:")
            raise
            
    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the drug-disease interaction analysis to a file."""
        if self.config is None:
            raise ValueError("No configuration information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        medicine_safe = self.config.medicine_name.lower().replace(' ', '_')
        condition_safe = self.config.condition_name.lower().replace(' ', '_')
        base_filename = f"{medicine_safe}_{condition_safe}_interaction"
        
        return save_model_response(result, output_dir / base_filename)
