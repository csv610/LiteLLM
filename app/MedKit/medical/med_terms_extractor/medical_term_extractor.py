#!/usr/bin/env python3
"""
Medical Term Extractor Analysis module.

This module provides the core MedicalTermExtractor class for extracting
and categorizing medical terms from text using LiteClient.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from medical_term_extractor_models import MedicalTermsModel, ModelOutput
from medical_term_extractor_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalTermExtractor:
    """Extracts and categorizes medical terms from text using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the extractor."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.text = None  # Store the text for later use in save
        logger.debug(f"Initialized MedicalTermExtractor")

    def generate_text(self, text: str, structured: bool = False) -> ModelOutput:
        """Extract medical terms from text."""
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty")

        # Store the text for later use in save
        self.text = text
        logger.debug(f"Starting medical term extraction for text length: {len(text)}")

        response_format = None
        if structured:
            response_format = MedicalTerms

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(text)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully extracted medical terms")
            return result
        except Exception as e:
            logger.error(f"✗ Error extracting medical terms: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical term extraction information to a file."""
        if self.text is None:
            raise ValueError("No text information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"medical_terms_extraction"
        
        return save_model_response(result, output_dir / base_filename)
