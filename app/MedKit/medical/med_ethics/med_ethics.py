#!/usr/bin/env python3
"""
Medical Ethics module.

This module provides the core MedEthicsGenerator class for generating
comprehensive medical ethics analysis based on provided configuration.
"""

import logging
from pathlib import Path
from typing import Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from med_ethics_models import EthicalAnalysisModel, ModelOutput
from med_ethics_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedEthicalQA:
    """Generates comprehensive medical ethics analysis."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.question = None  # Store the ethics question being analyzed
        logger.debug(f"Initialized MedEthicalQA")

    def generate_text(self, question: str, structured: bool = False) -> ModelOutput:
        """Generate comprehensive medical ethics analysis."""
        if not question or not str(question).strip():
            raise ValueError("Medical ethics question or scenario cannot be empty")

        # Store the question for later use in save
        self.question = question
        logger.debug(f"Starting medical ethics analysis for: {question[:50]}...")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(question)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = EthicalAnalysisModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated medical ethics analysis")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating medical ethics analysis: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical ethics analysis to a file."""
        if self.question is None:
            raise ValueError("No medical ethics question available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        # Use first 50 chars of question for filename, sanitized
        sanitized_q = "".join(c for c in self.question[:50] if c.isalnum() or c in (" ", "_")).rstrip()
        base_filename = sanitized_q.lower().replace(' ', '_')
        
        return save_model_response(result, output_dir / base_filename)
