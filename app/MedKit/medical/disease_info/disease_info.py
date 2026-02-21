#!/usr/bin/env python3
"""
Disease Information module.

This module provides the core DiseaseInfoGenerator class for generating
comprehensive disease information based on provided configuration.
"""

import logging
from pathlib import Path
from typing import Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from .disease_info_models import DiseaseInfoModel, ModelOutput
from .disease_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class DiseaseInfoGenerator:
    """Generates comprehensive disease information."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.disease = None  # Store the disease being analyzed
        logger.debug(f"Initialized DiseaseInfoGenerator")

    def generate_text(self, disease: str, structured: bool = False) -> ModelOutput:
        """Generate comprehensive disease information."""
        if not disease or not str(disease).strip():
            raise ValueError("Disease name cannot be empty")

        # Store the disease for later use in save
        self.disease = disease
        logger.debug(f"Starting disease information generation for: {disease}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(disease)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = DiseaseInfoModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated disease information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating disease information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the disease information to a file."""
        if self.disease is None:
            raise ValueError("No disease information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.disease.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)
