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
        """Generate a comprehensive medical specialists database using a 3-tier system."""
        logger.debug("Starting 3-tier medical speciality database generation")

        try:
            # --- Tier 1: Specialist Stages (JSON) ---
            logger.info("Agent 1 (Planner): Identifying major specialty categories")
            planner_input = ModelInput(
                system_prompt=PromptBuilder.create_planner_system_prompt(),
                user_prompt=PromptBuilder.create_planner_user_prompt(),
                response_format=CategoryList if structured else None,
            )
            categories_result = self.ask_llm(planner_input)
            
            categories = []
            if structured:
                categories = categories_result.data.categories
            else:
                raw_lines = str(categories_result.markdown).split('\n')
                for line in raw_lines:
                    cleaned = line.strip().strip('-* ')
                    if cleaned and len(cleaned) < 100:
                        categories.append(cleaned)
                if not categories:
                    categories = ["Internal Medicine", "Surgery", "Pediatrics", "Diagnostic", "Psychiatry"]

            all_specialists = []
            for category in categories:
                logger.info(f"Agent 2 (Researcher): Investigating category '{category}'")
                researcher_input = ModelInput(
                    system_prompt=PromptBuilder.create_researcher_system_prompt(),
                    user_prompt=PromptBuilder.create_researcher_user_prompt(category),
                    response_format=MedicalSpecialistDatabase if structured else None,
                )
                res_result = self.ask_llm(researcher_input)
                if structured:
                    all_specialists.extend(res_result.data.specialists)
                else:
                    all_specialists.append(f"Category: {category}\n{res_result.markdown}")

            specialist_data_json = ""
            if structured:
                spec_db = MedicalSpecialistDatabase(specialists=all_specialists)
                specialist_data_json = spec_db.model_dump_json(indent=2)
            else:
                specialist_data_json = "\n\n".join(all_specialists)

            # --- Tier 2: Compliance Auditor Stage (JSON Audit) ---
            logger.info("Agent 3 (Auditor): Auditing specialty data")
            reviewer_input = ModelInput(
                system_prompt=PromptBuilder.create_reviewer_system_prompt(),
                user_prompt=PromptBuilder.create_reviewer_user_prompt(specialist_data_json),
                response_format=None # Audit result
            )
            audit_result = self.ask_llm(reviewer_input)
            audit_json = audit_result.markdown

            # --- Tier 3: Final Output Synthesis (Markdown Closer) ---
            logger.info("Agent 4 (Output): Synthesizing final database")
            out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(
                specialist_data_json, audit_json
            )
            output_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.ask_llm(output_input)

            logger.info("✓ Successfully generated 3-tier medical specialty database")
            return ModelOutput(
                data=MedicalSpecialistDatabase(specialists=all_specialists) if structured else None,
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ Error in 3-tier generation workflow: {e}")
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
