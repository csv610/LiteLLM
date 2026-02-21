#!/usr/bin/env python3
"""
Medical Test Devices Analysis module.

This module provides the core MedicalTestDeviceGuide class for generating
comprehensive information for medical test devices using LiteClient.
"""

import logging
from pathlib import Path
from typing import Optional, Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from medical_test_devices_models import MedicalDeviceInfoModel, ModelOutput
from medical_test_devices_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalTestDeviceGuide:
    """Generate comprehensive information for medical test devices."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator.

        Args:
            model_config: ModelConfig object containing model settings.
        """
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.device_name = None  # Store the device name for later use in save
        logger.info(f"Initialized MedicalTestDeviceGuide using model: {model_config.model}")

    def generate_text(self, device_name: str, structured: bool = False) -> ModelOutput:
        """
        Generate comprehensive medical device information.

        Args:
            device_name: Name of the medical device.
            structured: Whether to use structured output mode (default: False)

        Returns:
            ModelOutput: The generated MedicalDeviceInfo object or raw string.
        """
        # Store the device name for later use in save
        self.device_name = device_name
        mode = "structured" if structured else "unstructured"
        logger.info(f"Generating {mode} medical device information for: '{device_name}'")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.build_user_prompt(device_name)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = MedicalDeviceInfoModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.info(f"Successfully generated information for '{device_name}'")
            return result
        except (ValueError, RuntimeError) as e:
            logger.error(f"Failed to generate information for '{device_name}': {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """
        Call the LLM client to generate information.

        Args:
            model_input: ModelInput object.

        Returns:
            The generated results (MedicalDeviceInfo or str).
        """
        logger.debug(f"Sending request to LLM client for model: {self.model_config.model}")
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_path: Path) -> Path:
        """Save the generated device information to a JSON or MD file."""
        if isinstance(result, str) and output_path.suffix == ".json":
            output_path = output_path.with_suffix(".md")
        
        logger.info(f"Saving device information to: {output_path}")
        return save_model_response(result, output_path)
