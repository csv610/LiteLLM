#!/usr/bin/env python3
"""
Medical Topic module.

This module provides the core MedicalTopicGenerator class for generating
comprehensive medical topic information based on provided configuration.
"""

import logging
from pathlib import Path
from typing import Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from medical_topic_models import MedicalTopicModel, ModelOutput
from medical_topic_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalTopicGenerator:
    """Generates comprehensive medical topic information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.topic = None  # Store the topic being analyzed
        logger.debug(f"Initialized MedicalTopicGenerator")

    def generate_text(self, topic: str, structured: bool = False) -> ModelOutput:
        """Generates comprehensive medical topic information."""
        if not topic or not str(topic).strip():
            raise ValueError("Topic name cannot be empty")

        # Store the topic for later use in save
        self.topic = topic
        logger.debug(f"Starting medical topic information generation for: {topic}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(topic)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = MedicalTopicModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated medical topic information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating medical topic information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical topic information to a file."""
        if self.topic is None:
            raise ValueError("No topic information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.topic.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)
