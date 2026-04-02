#!/usr/bin/env python3
"""
Medical Myths Checker module.

This module provides the core MedicalMythsChecker class for analyzing
medical myths for factual accuracy based on peer-reviewed evidence.
"""

import logging
from pathlib import Path
from typing import Optional

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

from .medical_myth_checker_models import MedicalMythAnalysisModel, ModelOutput
from .medical_myth_checker_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalMythsChecker:
    """Analyzes medical myths for factual accuracy based on peer-reviewed evidence."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the myths checker."""
        self.client = LiteClient(model_config=model_config)
        self.myth: Optional[str] = None

    def generate_text(self, myth: str, structured: bool = False) -> ModelOutput:
        """Analyze a medical myth using a 3-tier agent system."""
        if not myth or not myth.strip():
            raise ValueError("Myth statement cannot be empty")

        self.myth = myth
        logger.info(f"Starting 3-tier myth analysis for: {myth}")

        try:
            # 1. Specialist Stage (JSON)
            logger.debug("[Specialist] Analyzing myth evidence...")
            spec_input = ModelInput(
                system_prompt=PromptBuilder.system_prompt(),
                user_prompt=PromptBuilder.user_prompt(myth),
                response_format=MedicalMythAnalysisModel if structured else None,
            )
            spec_res = self._ask_llm(spec_input)
            
            if structured:
                spec_json = spec_res.data.model_dump_json(indent=2)
            else:
                spec_json = spec_res.markdown

            # 2. Auditor Stage (JSON Audit)
            logger.debug("[Auditor] Auditing evidence...")
            audit_sys, audit_usr = PromptBuilder.get_evidence_auditor_prompts(myth, spec_json)
            audit_input = ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None # Audit result
            )
            audit_res = self._ask_llm(audit_input)
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown Closer)
            logger.debug("[Output] Synthesizing final report...")
            out_sys, out_usr = PromptBuilder.get_output_synthesis_prompts(myth, spec_json, audit_json)
            out_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self._ask_llm(out_input)

            logger.info("✓ Successfully generated 3-tier myth analysis")
            return ModelOutput(
                data=spec_res.data, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier Myth generation failed: {e}")
            raise

    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """
        Internal helper to call the LLM client.
        """
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical myth analysis to a file."""
        if self.myth is None:
            raise ValueError("No myth information available. Call generate_text first.")

        # Generate base filename - save_model_response will add appropriate extension
        # Create a safe filename from the myth statement
        safe_myth = (
            self.myth.lower()[:50].replace(" ", "_").replace('"', "").replace("'", "")
        )
        base_filename = f"myth_analysis_{safe_myth}"

        return save_model_response(result, output_dir / base_filename)
