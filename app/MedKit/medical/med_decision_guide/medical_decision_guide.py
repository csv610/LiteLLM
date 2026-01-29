#!/usr/bin/env python3
"""
Medical Decision Guide Analysis module.

This module provides the core MedicalDecisionGuideGenerator class for generating
medical decision guides for symptom assessment.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from medical_decision_guide_models import MedicalDecisionGuideModel, ModelOutput
from medical_decision_guide_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalDecisionGuideGenerator:
    """Generates medical decision guides based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the medical decision guide generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.symptom = None  # Store the symptom for later use in save
        logger.debug(f"Initialized MedicalDecisionGuideGenerator")

    def generate_text(self, symptom: str, structured: bool = False) -> ModelOutput:
        """Generates a medical decision guide for symptom assessment."""
        # Store the symptom for later use in save
        self.symptom = symptom
        
        if not symptom or not str(symptom).strip():
            raise ValueError("Symptom name cannot be empty")

        logger.debug(f"Starting decision guide generation for: {symptom}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(symptom)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = MedicalDecisionGuideModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated medical decision guide")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating medical decision guide: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical decision guide information to a file."""
        if self.symptom is None:
            raise ValueError("No symptom information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.symptom.lower().replace(' ', '_')}_decision_guide"
        
        return save_model_response(result, output_dir / base_filename)
