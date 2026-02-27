#!/usr/bin/env python3
"""
Medical Topic module.

This module provides the core LegalRightsGenerator class for generating
comprehensive patient legal rights information based on provided configuration.
"""

import logging
from pathlib import Path
from typing import Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

try:
    from med_legal.legal_rights_models import LegalRightsModel, ModelOutput
    from med_legal.legal_rights_prompts import PromptBuilder
except (ImportError, ValueError):
    from legal_rights_models import LegalRightsModel, ModelOutput
    from legal_rights_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class LegalRightsGenerator:
    """Generates comprehensive patient legal rights information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.topic = None  # Store the topic being analyzed
        logger.debug(f"Initialized LegalRightsGenerator for Patient Legal Rights")

    def generate_text(self, topic: str, country: str, structured: bool = False) -> ModelOutput:
        """Generates comprehensive patient legal rights information for a specific country."""
        if not topic or not str(topic).strip():
            raise ValueError("Topic name cannot be empty")
        if not country or not str(country).strip():
            raise ValueError("Country cannot be empty")

        # Store the topic for later use in save
        self.topic = topic
        logger.debug(f"Starting patient legal rights information generation for: {topic} in {country}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(topic, country)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = LegalRightsModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated patient legal rights information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating patient legal rights information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path, user_name: str = "anonymous") -> Path:
        """Saves the legal rights information to a file with a specific naming convention."""
        from datetime import datetime
        if self.topic is None:
            raise ValueError("No topic information available. Call generate_text first.")
        
        # Use simple name for user, lowercase
        safe_user = "".join([c for c in user_name.lower() if c.isalnum() or c == '_'])
        
        # Format date like 'oct102026'
        date_str = datetime.now().strftime("%b%d%Y").lower()
        
        # New filename format: {user_name}_complain_{date}
        base_filename = f"{safe_user}_complain_{date_str}"
        
        return save_model_response(result, output_dir / base_filename)
