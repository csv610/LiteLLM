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
        """
        Analyze a statement using a multi-agent approach (Researcher, Skeptic, Synthesizer).
        Runs Researcher and Skeptic in parallel.
        """
        if not statement or not statement.strip():
            raise ValueError("Statement cannot be empty")

        self.statement = statement
        logger.info(f"Starting parallel multi-agent analysis for: {statement}")

        with ThreadPoolExecutor(max_workers=2) as executor:
            # Parallel Agent 1: Researcher (finds support)
            logger.info("Agent 1: Medical Researcher gathering evidence (Parallel)...")
            researcher_input = ModelInput(
                system_prompt=PromptBuilder.create_researcher_prompt(),
                user_prompt=PromptBuilder.create_user_prompt(statement)
            )
            future_researcher = executor.submit(self._ask_llm, researcher_input)

            # Parallel Agent 2: Skeptic (finds errors/red flags)
            logger.info("Agent 2: Medical Skeptic identifying red flags (Parallel)...")
            skeptic_input = ModelInput(
                system_prompt=PromptBuilder.create_skeptic_prompt(),
                user_prompt=PromptBuilder.create_user_prompt(statement)
            )
            future_skeptic = executor.submit(self._ask_llm, skeptic_input)

            # Wait for both reports
            researcher_report = future_researcher.result().markdown
            skeptic_report = future_skeptic.result().markdown

        # Agent 3: Lead Medical Examiner (Synthesizer)
        logger.info("Agent 3: Lead Medical Examiner synthesizing findings...")
        synthesizer_input = ModelInput(
            system_prompt=PromptBuilder.create_synthesizer_prompt(researcher_report, skeptic_report),
            user_prompt=PromptBuilder.create_user_prompt(statement)
        )
        synth_result = self._ask_llm(synthesizer_input)
        synth_report = synth_result.markdown

        # Agent 4: Medical Compliance & Safety Officer
        logger.info("Agent 4: Medical Compliance Officer performing safety review...")
        response_format = MedicalFactFictionAnalysisModel if structured else None
        compliance_input = ModelInput(
            system_prompt=PromptBuilder.create_compliance_officer_prompt(synth_report),
            user_prompt=PromptBuilder.create_user_prompt(statement),
            response_format=response_format
        )
        
        result = self._ask_llm(compliance_input)
        
        # Store intermediate reports for traceability
        result.researcher_report = researcher_report
        result.skeptic_report = skeptic_report
        
        logger.info("✓ Multi-agent analysis (including compliance) complete")
        return result

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
