#!/usr/bin/env python3
"""
Drug Addiction Analysis module.

This module provides the core DrugAddiction class for analyzing
the addictive potential and risks associated with medicines and substances.
"""

import logging
from pathlib import Path
from typing import Optional, Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from drug_addiction_models import DrugAddictionModel, ModelOutput
from drug_addiction_prompts import PromptBuilder, DrugAddictionInput

logger = logging.getLogger(__name__)


class DrugAddiction:
    """Analyzes drug addiction risks based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the drug addiction analyzer."""
        self.client = LiteClient(model_config)
        self.config = None  # Store the configuration for later use in save
        logger.debug(f"Initialized DrugAddiction")

    def generate_text(self, config: DrugAddictionInput, structured: bool = False) -> ModelOutput:
        """Analyzes addiction risks for a medicine or substance."""
        # Store the configuration for later use in save
        self.config = config
        logger.debug(f"Starting drug addiction analysis")
        logger.debug(f"Substance: {config.medicine_name}")

        # Create user prompt with context
        user_prompt = PromptBuilder.create_user_prompt(config)
        system_prompt = PromptBuilder.create_system_prompt()
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = DrugAddictionModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self._ask_llm(model_input)
            logger.debug("✓ Successfully analyzed addiction risks")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating drug addiction analysis: {e}")
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
        """Saves the drug addiction analysis information to a file."""
        if self.config is None:
            raise ValueError("No configuration available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.config.medicine_name.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)
