#!/usr/bin/env python3
"""
Drug-Food Interaction Analysis module.

This module provides the core DrugFoodInteraction class for analyzing
how food and beverages interact with medicines.
"""

import logging
from pathlib import Path
from typing import Optional, Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from drug_food_interaction_models import DrugFoodInteractionModel, ModelOutput
from drug_food_interaction_prompts import PromptBuilder, DrugFoodInput

logger = logging.getLogger(__name__)


class DrugFoodInteraction:
    """Analyzes drug-food interactions based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the drug-food interaction analyzer."""
        self.client = LiteClient(model_config)
        self.config = None  # Store the configuration for later use in save
        logger.debug(f"Initialized DrugFoodInteraction")

    def generate_text(self, config: DrugFoodInput, structured: bool = False) -> ModelOutput:
        """Analyzes how food and beverages interact with a medicine."""
        # Store the configuration for later use in save
        self.config = config
        logger.debug(f"Starting drug-food interaction analysis")
        logger.debug(f"Medicine: {config.medicine_name}")

        # Create user prompt with context
        user_prompt = PromptBuilder.create_user_prompt(config)
        system_prompt = PromptBuilder.create_system_prompt()
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = DrugFoodInteractionModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self._ask_llm(model_input)
            logger.debug("✓ Successfully analyzed food interactions")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating drug-food interaction: {e}")
            raise

    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Helper to call LiteClient with error handling."""
        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"✗ Error during LLM analysis: {e}")
            logger.exception("Full exception details:")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the drug-food interaction information to a file."""
        if self.config is None:
            raise ValueError("No configuration available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.config.medicine_name.lower().replace(' ', '_')}_food_interaction"
        
        return save_model_response(result, output_dir / base_filename)
