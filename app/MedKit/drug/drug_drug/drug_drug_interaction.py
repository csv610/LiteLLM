#!/usr/bin/env python3
"""
Drug-Drug Interaction Analysis module.

This module provides the core DrugDrugInteractionGenerator class for analyzing
interactions between two medicines.
"""

import logging
from pathlib import Path
from typing import Optional, Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from .drug_drug_interaction_models import DrugInteractionModel, ModelOutput
from .drug_drug_interaction_prompts import DrugDrugPromptBuilder, DrugDrugInput

logger = logging.getLogger(__name__)


class DrugDrugInteractionGenerator:
    """Generates drug-drug interaction analysis."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.user_input = None  # Store the configuration for later use in save
        logger.debug(f"Initialized DrugDrugInteractionGenerator")

    def generate_text(self, user_input: DrugDrugInput, structured: bool = False) -> ModelOutput:
        """Generate drug-drug interaction analysis."""
        # Store the configuration for later use in save
        self.user_inout = user_input
        logger.debug(f"Starting drug-drug interaction analysis")
        logger.debug(f"Drug 1: {user_input.medicine1}")
        logger.debug(f"Drug 2: {user_input.medicine2}")

        # Create user prompt with context
        user_prompt = DrugDrugPromptBuilder.create_user_prompt(user_input)
        system_prompt = DrugDrugPromptBuilder.create_system_prompt()
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = DrugInteractionModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully analyzed drug-drug interaction")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating drug-drug interaction: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the drug-drug interaction information to a file."""
        if self.user_input is None:
            raise ValueError("No configuration available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.user_input.medicine1.lower().replace(' ', '_')}_{self.user_input.medicine2.lower().replace(' ', '_')}_interaction"
        
        return save_model_response(result, output_dir / base_filename)
