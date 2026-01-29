#!/usr/bin/env python3
"""
Medical Test Information Analysis module.

This module provides the core MedicalTestInfoGenerator class for generating
comprehensive information for medical tests using LiteClient.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from medical_test_info_models import MedicalTestInfoModel, ModelOutput
from medical_test_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalTestInfoGenerator:
    """Generate comprehensive information for medical tests."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator.

        Args:
            model_config: ModelConfig object containing model settings.
        """
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.test_name = None  # Store the test name for later use in save
        logger.debug(f"Initialized MedicalTestInfoGenerator using model: {model_config.model}")

    def generate_text(self, test_name: str, structured: bool = False) -> ModelOutput:
        """
        Generate the core medical test information.

        Args:
            test_name: The name of the medical test.
            structured: Whether to use structured output mode (default: False)

        Returns:
            ModelOutput: Validated evaluation results or raw string
        """
        # Store the test name for later use in save
        self.test_name = test_name
        logger.debug(f"Generating medical test information for: {test_name}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(test_name)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = MedicalTestInfoModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated medical test information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating medical test information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """
        Call the LLM client to generate information.

        Args:
            model_input: ModelInput object.

        Returns:
            The generated results (MedicalTestInfo or str).
        """
        logger.debug(f"Sending request to LLM client for model: {self.model_config.model}")
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical test information to a file."""
        if self.test_name is None:
            raise ValueError("No test name information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.test_name.lower().replace(' ', '_')}_test_info"
        
        return save_model_response(result, output_dir / base_filename)
