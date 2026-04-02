#!/usr/bin/env python3
"""
Patient Medical History Analysis module.

This module provides the core PatientMedicalHistoryGenerator class for generating
patient medical history questions using LiteClient.
"""

import logging
from pathlib import Path

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

from .patient_medical_history_models import ModelOutput, PatientMedicalHistoryModel
from .patient_medical_history_prompts import MedicalHistoryInput, PromptBuilder

logger = logging.getLogger(__name__)


class PatientMedicalHistoryGenerator:
    """Generates patient medical history questions using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.user_input = None  # Store the input for later use in save
        logger.debug("Initialized PatientMedicalHistoryGenerator")

    def generate_text(
        self, user_input: MedicalHistoryInput, structured: bool = False
    ) -> ModelOutput:
        """Generate 3-tier medical history questionnaire."""
        self.user_input = user_input
        logger.info(f"Starting 3-tier medical history generation for: {user_input.exam}")

        try:
            # 1. Specialist Stage (JSON)
            logger.debug("[Specialist] Generating questions...")
            system_prompt = PromptBuilder.create_system_prompt()
            user_prompt = PromptBuilder.create_user_prompt(user_input)
            
            spec_input = ModelInput(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format=PatientMedicalHistoryModel if structured else None,
            )
            spec_res = self.ask_llm(spec_input)
            
            if structured:
                spec_json = spec_res.data.model_dump_json(indent=2)
            else:
                spec_json = spec_res.markdown

            # 2. Auditor Stage (JSON Audit)
            logger.debug("[Auditor] Auditing questions...")
            audit_sys, audit_usr = PromptBuilder.get_history_auditor_prompts(user_input, spec_json)
            audit_input = ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None # Audit result
            )
            audit_res = self.ask_llm(audit_input)
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown Closer)
            logger.debug("[Output] Synthesizing final questionnaire...")
            out_sys, out_usr = PromptBuilder.get_output_synthesis_prompts(user_input, spec_json, audit_json)
            out_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.ask_llm(out_input)

            logger.info("✓ Successfully generated 3-tier medical history questionnaire")
            return ModelOutput(
                data=spec_res.data if structured else None, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier History generation failed: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the patient medical history information to a file."""
        if self.user_input is None:
            raise ValueError(
                "No input information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = (
            f"{self.user_input.exam.lower().replace(' ', '_')}_medical_history"
        )

        return save_model_response(result, output_dir / base_filename)
