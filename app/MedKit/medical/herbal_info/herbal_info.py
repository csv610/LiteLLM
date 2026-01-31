#!/usr/bin/env python3
"""
Herbal Information module.

This module provides the core HerbalInfoGenerator class for generating
comprehensive herbal remedy information based on provided configuration.
"""

import logging
from pathlib import Path
from typing import Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from herbal_info_models import HerbalInfoModel, ModelOutput
from herbal_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class HerbalInfoGenerator:
    """Generates comprehensive herbal remedy information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.herb = None  # Store the herb being analyzed
        logger.debug(f"Initialized HerbalInfoGenerator")

    def generate_text(self, herb: str, structured: bool = False) -> ModelOutput:
        """Generates comprehensive herbal information."""
        # Validate inputs
        if not herb or not str(herb).strip():
            raise ValueError("Herb name cannot be empty")

        # Store the herb for later use in save
        self.herb = herb
        logger.debug(f"Starting herbal information generation for: {herb}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(herb)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = HerbalInfoModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated herbal information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating herbal information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the herbal information to a file."""
        if self.herb is None:
            raise ValueError("No herb information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.herb.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)
