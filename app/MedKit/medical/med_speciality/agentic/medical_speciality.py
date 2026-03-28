#!/usr/bin/env python3
"""
Medical Speciality Analysis module.

This module provides the core MedicalSpecialityGenerator class for generating
a comprehensive database of medical specialities using LiteClient.
"""

import logging
from pathlib import Path
from typing import Union

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

from .medical_speciality_models import CategoryList, MedicalSpecialistDatabase
from .medical_speciality_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalSpecialityGenerator:
    """Generate a comprehensive database of medical specialities using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        logger.debug("Initialized MedicalSpecialityGenerator")

    def generate_text(
        self, structured: bool = False
    ) -> Union[MedicalSpecialistDatabase, str]:
        """Generate a comprehensive medical specialists database using multiple agents."""
        logger.debug("Starting multi-agent medical speciality database generation")

        try:
            # --- Agent 1: The Planner ---
            logger.info("Agent 1 (Planner): Identifying major specialty categories")
            planner_input = ModelInput(
                system_prompt=PromptBuilder.create_planner_system_prompt(),
                user_prompt=PromptBuilder.create_planner_user_prompt(),
                response_format=CategoryList if structured else None,
            )
            
            categories_result = self.ask_llm(planner_input)
            
            categories = []
            if structured:
                categories = categories_result.categories
            else:
                # If unstructured, split by newline and filter out empty strings
                raw_lines = str(categories_result).split('\n')
                for line in raw_lines:
                    cleaned = line.strip().strip('-* ')
                    if cleaned and len(cleaned) < 100:
                        categories.append(cleaned)
                
                # Fallback if parsing fails
                if not categories:
                    categories = ["Internal Medicine", "Surgery", "Pediatrics", "Diagnostic", "Psychiatry"]

            logger.info(f"Planner identified {len(categories)} categories")

            # --- Agent 2: The Researchers ---
            all_structured_specialists = []
            all_specialists_text = []

            for category in categories:
                logger.info(f"Agent 2 (Researcher): Investigating category '{category}'")
                researcher_input = ModelInput(
                    system_prompt=PromptBuilder.create_researcher_system_prompt(),
                    user_prompt=PromptBuilder.create_researcher_user_prompt(category),
                    response_format=MedicalSpecialistDatabase if structured else None,
                )
                
                researcher_result = self.ask_llm(researcher_input)
                
                if structured:
                    all_structured_specialists.extend(researcher_result.specialists)
                else:
                    all_specialists_text.append(f"--- Category: {category} ---\n{researcher_result}")

            # --- Agent 3: The Reviewer/Aggregator ---
            logger.info("Agent 3 (Reviewer): Aggregating findings")
            if structured:
                # For structured data, we aggregate programmatically to guarantee formatting
                logger.info("✓ Successfully generated and aggregated structured database")
                return MedicalSpecialistDatabase(specialists=all_structured_specialists)
            else:
                combined_data = "\n\n".join(all_specialists_text)
                reviewer_input = ModelInput(
                    system_prompt=PromptBuilder.create_reviewer_system_prompt(),
                    user_prompt=PromptBuilder.create_reviewer_user_prompt(combined_data),
                    response_format=None,
                )
                
                final_result = self.ask_llm(reviewer_input)
                logger.info("✓ Successfully generated and reviewed text database")
                return final_result

        except Exception as e:
            logger.error(f"✗ Error in multi-agent generation workflow: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> Union[MedicalSpecialistDatabase, str]:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)

    def save(
        self, result: Union[MedicalSpecialistDatabase, str], output_dir: Path
    ) -> Path:
        """Saves the medical speciality database information to a file."""
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = "medical_specialities_database"

        return save_model_response(result, output_dir / base_filename)
