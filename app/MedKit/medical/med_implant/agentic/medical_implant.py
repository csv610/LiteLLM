#!/usr/bin/env python3
"""
Medical Implant module.

This module provides the core MedicalImplantGenerator class for generating
comprehensive medical implant information based on provided configuration.
"""

import logging
from pathlib import Path

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

try:
    from .medical_implant_models import MedicalImplantInfoModel, ModelOutput
    from .medical_implant_prompts import PromptBuilder
except (ImportError, ValueError):
    from medical.med_implant.agentic.medical_implant_models import (
        MedicalImplantInfoModel,
        ModelOutput,
    )
    from medical.med_implant.agentic.medical_implant_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalImplantGenerator:
    """Generates comprehensive medical implant information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.implant = None  # Store the implant being analyzed
        logger.debug("Initialized MedicalImplantGenerator")

    def generate_text(self, implant: str, structured: bool = False) -> ModelOutput:
        """Generates 3-tier comprehensive medical implant information."""
        if not implant or not str(implant).strip():
            raise ValueError("Implant name cannot be empty")

        self.implant = implant
        logger.info(f"Starting 3-tier implant generation for: {implant}")

        try:
            # 1. Specialist Stage (JSON)
            logger.debug(f"[Specialist] Generating content for: {implant}")
            system_prompt = PromptBuilder.create_system_prompt()
            user_prompt = PromptBuilder.create_user_prompt(implant)
            
            spec_input = ModelInput(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format=MedicalImplantInfoModel if structured else None,
            )
            spec_res = self.ask_llm(spec_input)
            
            if structured:
                spec_json = spec_res.data.model_dump_json(indent=2)
            else:
                spec_json = spec_res.markdown

            # 2. Auditor Stage (JSON Audit)
            logger.debug(f"[Auditor] Auditing content for: {implant}")
            audit_sys, audit_usr = PromptBuilder.get_implant_auditor_prompts(implant, spec_json)
            audit_input = ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None # Audit result
            )
            audit_res = self.ask_llm(audit_input)
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown Closer)
            logger.debug(f"[Output] Synthesizing final report for: {implant}")
            out_sys, out_usr = PromptBuilder.get_output_synthesis_prompts(implant, spec_json, audit_json)
            out_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.ask_llm(out_input)

            logger.info("✓ Successfully generated 3-tier implant information")
            return ModelOutput(
                data=spec_res.data if structured else None, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier implant generation failed: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the implant information to a file."""
        if self.implant is None:
            raise ValueError(
                "No implant information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.implant.lower().replace(' ', '_')}"

        return save_model_response(result, output_dir / base_filename)
