#!/usr/bin/env python3
"""
Med Image Classification Information Analysis module.

This module provides the core MedImageClassifier class for generating
comprehensive information for med image classifications using LiteClient.
"""

import logging
from pathlib import Path

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from med_images_models import MedImagesModel, MedicalImageClassificationModel, ModelOutput
from med_images_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedImageClassifier:
    """Generate comprehensive information for med image classifications."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator.

        Args:
            model_config: ModelConfig object containing model settings.
        """
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.test_name = None  # Store the test name for later use in save
        logger.debug(f"Initialized MedImageClassifier using model: {model_config.model}")

    def generate_text(self, test_name: str, structured: bool = False) -> ModelOutput:
        """
        Generate the core med image classification information.

        Args:
            test_name: The name of the med image classification.
            structured: Whether to use structured output mode (default: False)

        Returns:
            ModelOutput: Validated evaluation results or raw string
        """
        # Store the test name for later use in save
        self.test_name = test_name
        logger.debug(f"Generating med image classification information for: {test_name}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(test_name)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = MedImagesModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated med image classification information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating med image classification information: {e}")
            raise

    def classify_image(self, image_path: str, structured: bool = True) -> ModelOutput:
        """
        Classify a medical image.

        Args:
            image_path: Path to the medical image file.
            structured: Whether to use structured output mode (default: True)

        Returns:
            ModelOutput: Validated classification results or raw string
        """
        image_path_obj = Path(image_path)
        self.test_name = image_path_obj.stem
        logger.debug(f"Classifying medical image: {image_path}")

        system_prompt = PromptBuilder.create_image_classification_system_prompt()
        user_prompt = PromptBuilder.create_image_classification_user_prompt()
        
        response_format = None
        if structured:
            response_format = MedicalImageClassificationModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            image_path=image_path,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text() for image classification...")
        try:
            result = self.ask_llm(model_input)
            logger.debug(f"✓ Successfully classified medical image: {image_path}")
            return result
        except Exception as e:
            logger.error(f"✗ Error classifying medical image {image_path}: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """
        Call the LLM client to generate information.

        Args:
            model_input: ModelInput object.

        Returns:
            The generated results (MedImages or str).
        """
        logger.debug(f"Sending request to LLM client for model: {self.model_config.model}")
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the med image classification information to a file."""
        if self.test_name is None:
            raise ValueError("No test name information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.test_name.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)
