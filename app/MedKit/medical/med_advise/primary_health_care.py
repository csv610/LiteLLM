#!/usr/bin/env python3
"""
Primary Health Care module.

This module provides the PrimaryHealthCareProvider class for addressing
patient questions with a generalist medical perspective.
"""

import logging
from pathlib import Path
from typing import Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from primary_health_care_models import PrimaryCareResponseModel, ModelOutput
from primary_health_care_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class PrimaryHealthCareProvider:
    """Provides general medical information and guidance from a primary care perspective."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.query = None  # Store the query being addressed
        logger.debug(f"Initialized PrimaryHealthCareProvider")

    def generate_text(self, query: str, structured: bool = False) -> ModelOutput:
        """Addresses a patient's health concern or question."""
        if not query or not str(query).strip():
            raise ValueError("Query cannot be empty")

        # Store the query for later use in save
        self.query = query
        logger.debug(f"Addressing health concern: {query}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(query)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = PrimaryCareResponseModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.client.generate_text(model_input=model_input)
            
            # If the result is a string, wrap it in ModelOutput
            if isinstance(result, str):
                result = ModelOutput(markdown=result)
            elif hasattr(result, 'data') and not hasattr(result, 'markdown'):
                # Handle cases where result might be a Pydantic model directly if structured=True
                result = ModelOutput(data=result)
            
            logger.debug("✓ Successfully generated response")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating response: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the provider's response to a file."""
        if self.query is None:
            raise ValueError("No query information available. Call address_concern first.")
        
        # Generate base filename from query - take first few words
        safe_query = "".join([c if c.isalnum() else "_" for c in self.query[:30].lower()]).strip("_")
        base_filename = f"response_{safe_query}"
        
        return save_model_response(result, output_dir / base_filename)
