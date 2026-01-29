#!/usr/bin/env python3
"""
Medical FAQ Analysis module.

This module provides the core MedicalFAQGenerator class for generating
comprehensive FAQ content for medical topics.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from medical_faq_models import MedicalFAQModel, ModelOutput
from medical_faq_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalFAQGenerator:
    """Generates comprehensive FAQ content."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the FAQ generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.topic = None  # Store the topic for later use in save
        logger.debug(f"Initialized MedicalFAQGenerator")

    def generate_text(
        self,
        topic: str,
        structured: bool = False
    ) -> ModelOutput:
        """Generate comprehensive FAQ content.

        Args:
            topic: Medical topic for FAQ generation
            structured: Whether to use structured output (Pydantic model)

        Returns:
            ModelOutput: Structured or plain text result
        """
        if not topic or not str(topic).strip():
            raise ValueError("Topic name cannot be empty")

        # Store the topic for later use in save
        self.topic = topic
        logger.debug(f"Starting FAQ generation for: {topic}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(topic)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = MedicalFAQModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated FAQ")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating FAQ: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical FAQ information to a file."""
        if self.topic is None:
            raise ValueError("No topic information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.topic.lower().replace(' ', '_')}_faq"
        
        return save_model_response(result, output_dir / base_filename)
