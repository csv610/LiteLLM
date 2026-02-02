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

from organ_disease_info_models import DiseaseInfoModel, OrganDiseasesModel, ModelOutput
from organ_disease_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class DiseaseInfoGenerator:
    """Generates comprehensive disease information."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.disease = None  # Store the disease being analyzed
        self.organ = None    # Store the organ being analyzed
        logger.debug(f"Initialized DiseaseInfoGenerator")

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def generate_text(self, organ: str, structured: bool = False) -> ModelOutput:
        """Generate diseases associated with an organ."""
        if not organ or not str(organ).strip():
            raise ValueError("Organ name cannot be empty")

        self.organ = organ
        self.disease = None
        logger.debug(f"Starting organ diseases generation for: {organ}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(organ)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = OrganDiseasesModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated organ diseases information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating organ diseases information: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the disease information to a file."""
        if self.disease:
            base_filename = f"{self.disease.lower().replace(' ', '_')}"
        elif self.organ:
            base_filename = f"{self.organ.lower().replace(' ', '_')}_diseases"
        else:
            raise ValueError("No disease or organ information available. Call generate_text or generate_organ_diseases first.")
        
        return save_model_response(result, output_dir / base_filename)
