#!/usr/bin/env python3
"""
Medical Implant module.

This module provides the core MedicalImplantGenerator class for generating
comprehensive medical implant information based on provided configuration.
"""

import logging
import sys
from pathlib import Path
from typing import Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from medical_implant_models import MedicalImplantInfoModel, ModelOutput
from medical_implant_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalImplantGenerator:
    """Generates comprehensive medical implant information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.implant = None  # Store the implant being analyzed
        logger.debug(f"Initialized MedicalImplantGenerator")

    def generate_text(self, implant: str, structured: bool = False) -> ModelOutput:
        """Generates comprehensive medical implant information."""
        if not implant or not str(implant).strip():
            raise ValueError("Implant name cannot be empty")

        # Store the implant for later use in save
        self.implant = implant
        logger.debug(f"Starting medical implant information generation for: {implant}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(implant)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
           response_format = MedicalImplantInfoModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated implant information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating implant information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the implant information to a file."""
        if self.implant is None:
            raise ValueError("No implant information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.implant.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)
