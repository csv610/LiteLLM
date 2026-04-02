#!/usr/bin/env python3
"""
Medical Facts Checker Analysis module.

This module provides the core MedicalFactsChecker class for analyzing
medical statements for factual accuracy.
"""

import logging
from pathlib import Path
from typing import Optional

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

try:
    from .medical_facts_checker_models import MedicalFactFictionAnalysisModel, ModelOutput
    from .medical_facts_checker_prompts import PromptBuilder
except ImportError:
    from medical_facts_checker_models import MedicalFactFictionAnalysisModel, ModelOutput
    from medical_facts_checker_prompts import PromptBuilder

logger = logging.getLogger(__name__)


from concurrent.futures import ThreadPoolExecutor

class MedicalFactsChecker:
    """Analyzes medical statements for factual accuracy."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the facts checker."""
        self.client = LiteClient(model_config=model_config)
        self.statement: Optional[str] = None
        self.output_path: Optional[Path] = None
        logger.debug("Initialized MedicalFactsChecker")

    def generate_text(self, statement: str, structured: bool = False) -> ModelOutput:
        """Analyze a statement using a 3-tier agent system."""
        if not statement or not statement.strip():
            raise ValueError("Statement cannot be empty")

        self.statement = statement
        logger.info(f"Starting 3-tier analysis for: {statement}")

        try:
            # --- Tier 1: Specialist Stage (Parallel & Sequential JSON) ---
            with ThreadPoolExecutor(max_workers=2) as executor:
                # Parallel specialists
                f_res = executor.submit(self._ask_llm, ModelInput(
                    system_prompt=PromptBuilder.create_researcher_prompt(),
                    user_prompt=PromptBuilder.create_user_prompt(statement)
                ))
                f_skp = executor.submit(self._ask_llm, ModelInput(
                    system_prompt=PromptBuilder.create_skeptic_prompt(),
                    user_prompt=PromptBuilder.create_user_prompt(statement)
                ))
                res_md = f_res.result().markdown
                skp_md = f_skp.result().markdown

            # Lead Specialist Synthesis
            synth_res = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_synthesizer_prompt(res_md, skp_md),
                user_prompt=PromptBuilder.create_user_prompt(statement)
            ))
            spec_json = synth_res.markdown

            # --- Tier 2: Compliance Auditor Stage (JSON Audit) ---
            audit_res = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_compliance_officer_prompt(spec_json),
                user_prompt=PromptBuilder.create_user_prompt(statement),
                response_format=MedicalFactFictionAnalysisModel if structured else None
            ))
            
            if structured:
                audit_json = audit_res.data.model_dump_json(indent=2)
            else:
                audit_json = audit_res.markdown

            # --- Tier 3: Final Output Synthesis (Markdown Closer) ---
            out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(
                statement, spec_json, audit_json
            )
            final_res = self._ask_llm(ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None
            ))

            logger.info("✓ Successfully generated 3-tier medical facts analysis")
            return ModelOutput(data=audit_res.data if structured else None, markdown=final_res.markdown)

        except Exception as e:
            logger.error(f"✗ 3-tier Facts generation failed: {e}")
            raise

    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """
        Internal helper to call the LLM client.
        """
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical facts analysis to a file."""
        if self.statement is None:
            raise ValueError(
                "No statement information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.statement.lower().replace(' ', '_')}_facts_analysis"

        return save_model_response(result, output_dir / base_filename)
