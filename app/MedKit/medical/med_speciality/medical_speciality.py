#!/usr/bin/env python3
"""
Medical Speciality Analysis module.

This module provides the core MedicalSpecialityGenerator class for generating
a comprehensive database of medical specialities using LiteClient.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from medical_speciality_models import MedicalSpecialistDatabase
from medical_speciality_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalSpecialityGenerator:
    """Generate a comprehensive database of medical specialities using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        logger.debug(f"Initialized MedicalSpecialityGenerator")

    def generate_text(self, structured: bool = False) -> Union[MedicalSpecialistDatabase, str]:
        """Generate a comprehensive medical specialists database."""
        logger.debug("Starting medical speciality database generation")

        response_format = None
        if structured:
            response_format = MedicalSpecialistDatabase

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt()
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
            logger.debug("✓ Successfully generated medical speciality database")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating medical speciality database: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> Union[MedicalSpecialistDatabase, str]:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: Union[MedicalSpecialistDatabase, str], output_dir: Path) -> Path:
        """Saves the medical speciality database information to a file."""
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"medical_specialities_database"
        
        return save_model_response(result, output_dir / base_filename)
