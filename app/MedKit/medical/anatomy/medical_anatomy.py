#!/usr/bin/env python3
"""
Medical Anatomy module.

This module provides the core MedicalAnatomyGenerator class for generating
comprehensive anatomical information based on provided configuration.
"""

import logging
from pathlib import Path
from typing import Optional, Union


from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from medical_anatomy_models import MedicalAnatomyModel, ModelOutput
from medical_anatomy_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalAnatomyGenerator:
    """Generates comprehensive anatomical information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.body_part = None  # Store the body part being analyzed
        logger.debug(f"Initialized MedicalAnatomyGenerator")

    def generate_text(self, body_part: str, structured: bool = False) -> ModelOutput:
        """Generates comprehensive anatomical information."""
        if not body_part or not str(body_part).strip():
            raise ValueError("Body part name cannot be empty")

        # Store the body part for later use in save
        self.body_part = body_part
        logger.debug(f"Starting anatomical information generation for: {body_part}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(body_part)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = MedicalAnatomyModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated anatomical information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating anatomical information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the anatomical information to a file."""
        if self.body_part is None:
            raise ValueError("No body part information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.body_part.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)
