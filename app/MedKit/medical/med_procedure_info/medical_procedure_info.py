#!/usr/bin/env python3
"""
Medical Procedure Information module.

This module provides the core MedicalProcedureInfoGenerator class for generating
comprehensive medical procedure information based on provided configuration.
"""

import logging
from pathlib import Path
from typing import Optional, Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from medical_procedure_info_models import MedicalProcedureInfoModel, ModelOutput
from medical_procedure_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalProcedureInfoGenerator:
    """Generate comprehensive information for medical procedures using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.procedure_name: Optional[str] = None
        logger.debug(f"Initialized MedicalProcedureInfoGenerator")

    def generate_text(self, procedure: str, structured: bool = False) -> ModelOutput:
        """Generate and retrieve comprehensive medical procedure information."""
        if not procedure or not procedure.strip():
            raise ValueError("Procedure name cannot be empty")

        # Store the procedure for later use in save
        self.procedure_name = procedure
        logger.debug(f"Starting medical procedure information generation for: {procedure}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(procedure)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = MedicalProcedureInfoModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated medical procedure information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating medical procedure information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical procedure information to a file."""
        if self.procedure_name is None:
            raise ValueError("No procedure information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.procedure_name.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)
