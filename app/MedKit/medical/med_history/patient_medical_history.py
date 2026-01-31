#!/usr/bin/env python3
"""
Patient Medical History Analysis module.

This module provides the core PatientMedicalHistoryGenerator class for generating
patient medical history questions using LiteClient.
"""

import logging
from pathlib import Path
from typing import Optional, Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from patient_medical_history_models import PatientMedicalHistoryModel, ModelOutput
from patient_medical_history_prompts import PromptBuilder, MedicalHistoryInput

logger = logging.getLogger(__name__)


class PatientMedicalHistoryGenerator:
    """Generates patient medical history questions using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.user_input = None  # Store the input for later use in save
        logger.debug(f"Initialized PatientMedicalHistoryGenerator")

    def generate_text(self, user_input: MedicalHistoryInput, structured: bool = False) -> ModelOutput:
        """Generate patient medical history questions."""
        # Store the input for later use in save
        self.user_input = user_input
        logger.debug(f"Starting medical history generation for: {user_input.exam}")

        response_format = None
        if structured:
            response_format = PatientMedicalHistoryModel

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(user_input)
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
            logger.debug("✓ Successfully generated medical history questions")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating medical history questions: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the patient medical history information to a file."""
        if self.user_input is None:
            raise ValueError("No input information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.user_input.exam.lower().replace(' ', '_')}_medical_history"
        
        return save_model_response(result, output_dir / base_filename)
