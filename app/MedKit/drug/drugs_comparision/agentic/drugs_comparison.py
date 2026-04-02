#!/usr/bin/env python3
"""
Drugs Comparison module.

This module provides the core DrugsComparison class for comparing two medicines
across clinical, regulatory, and practical metrics.
"""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

try:
    from .drugs_comparison_models import MedicinesComparisonResult
    from .drugs_comparison_prompts import PromptBuilder
except ImportError:
    from drugs_comparison_models import MedicinesComparisonResult
    from drugs_comparison_prompts import PromptBuilder

logger = logging.getLogger(__name__)


@dataclass
class DrugsComparisonInput:
    """Configuration and input for medicines comparison."""

    medicine1: str
    medicine2: str
    use_case: Optional[str] = None
    patient_age: Optional[int] = None
    patient_conditions: Optional[str] = None
    prompt_style: str = "detailed"


class DrugsComparison:
    """Compares two medicines using a multi-agent architecture."""

    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)
        self.config = None
        logger.debug("Initialized Multi-Agent DrugsComparison")

    def generate_text(
        self, config: DrugsComparisonInput, structured: bool = False
    ) -> Union[MedicinesComparisonResult, str]:
        """Compares two medicines using a 3-tier multi-agent system."""
        self.config = config
        self._validate_input(config)

        logger.info(f"Starting 3-tier analysis: {config.medicine1} vs {config.medicine2}")
        context = self._prepare_context(config)

        # 1. Tier 1: Specialist Agents (Parallelizable JSON)
        logger.debug("Tier 1: Running specialist agents...")
        pharmacology_report = self._run_agent(
            PromptBuilder.create_pharmacology_system_prompt(), config, context
        )
        regulatory_report = self._run_agent(
            PromptBuilder.create_regulatory_system_prompt(), config, context
        )
        market_report = self._run_agent(
            PromptBuilder.create_market_access_system_prompt(), config, context
        )
        context_report = self._run_agent(
            PromptBuilder.create_clinical_context_system_prompt(), config, context
        )
        compliance_report = self._run_agent(
            PromptBuilder.create_compliance_system_prompt(), config, context
        )

        specialist_data = f"""
        - Pharmacology: {pharmacology_report}
        - Regulatory: {regulatory_report}
        - Market Access: {market_report}
        - Clinical Context: {context_report}
        - Compliance: {compliance_report}
        """

        # 2. Tier 2: Safety Auditor (JSON Audit)
        logger.debug("Tier 2: Running safety auditor...")
        safety_report = self._run_agent(
            PromptBuilder.create_safety_auditor_system_prompt(), config, specialist_data
        )

        # 3. Tier 3: Final Output Synthesis (Markdown Closer)
        logger.debug("Tier 3: Output synthesis starting...")
        out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(
            config.medicine1, config.medicine2, specialist_data, safety_report
        )

        model_input = ModelInput(
            system_prompt=out_sys,
            user_prompt=out_usr,
            response_format=None,
        )

        final_res = self._ask_llm(model_input)
        
        # Assemble data if structured requested
        if structured:
            # We need to run the original synthesis agent if we want a structured model return
            # For now, let's assume we return the synthesized markdown as requested.
            pass

        logger.debug("✓ 3-tier Multi-agent synthesis complete")
        return ModelOutput(
            data=None, # Tier 1 data is complex here, can be added if needed
            markdown=final_res.markdown,
            metadata={"audit": safety_report}
        )

    def _run_agent(self, system_prompt: str, config: DrugsComparisonInput, context: str) -> str:
        """Helper to run a specific agent and get its narrative report."""
        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=PromptBuilder.create_user_prompt(
                config.medicine1, config.medicine2, context
            ),
        )
        # Specialist agents always return text reports for the synthesis orchestrator
        return self._ask_llm(model_input)

    def _validate_input(self, config: DrugsComparisonInput) -> None:
        """Validate input parameters."""
        if not config.medicine1 or not config.medicine1.strip():
            raise ValueError("Medicine 1 name cannot be empty")
        if not config.medicine2 or not config.medicine2.strip():
            raise ValueError("Medicine 2 name cannot be empty")
        if config.patient_age is not None and (
            config.patient_age < 0 or config.patient_age > 150
        ):
            raise ValueError("Age must be between 0 and 150 years")

    def _prepare_context(self, config: DrugsComparisonInput) -> str:
        """Build the analysis context string from input parameters."""
        context_parts = [f"Comparing {config.medicine1} and {config.medicine2}"]
        if config.use_case:
            context_parts.append(f"Use case: {config.use_case}")
            logger.debug(f"Use case: {config.use_case}")
        if config.patient_age is not None:
            context_parts.append(f"Patient age: {config.patient_age} years")
            logger.debug(f"Patient age: {config.patient_age}")
        if config.patient_conditions:
            context_parts.append(f"Patient conditions: {config.patient_conditions}")
            logger.debug(f"Patient conditions: {config.patient_conditions}")
        return ". ".join(context_parts) + "."

    def _ask_llm(
        self, model_input: ModelInput
    ) -> Union[MedicinesComparisonResult, str]:
        """Helper to call LiteClient with error handling."""
        logger.debug("Calling LiteClient.generate_text()...")
        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"✗ Error during LLM analysis: {e}")
            logger.exception("Full exception details:")
            raise

    def save(
        self, result: Union[MedicinesComparisonResult, str], output_dir: Path
    ) -> Path:
        """Saves the drugs comparison analysis to a file."""
        if self.config is None:
            raise ValueError(
                "No configuration information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        medicine1_safe = self.config.medicine1.lower().replace(" ", "_")
        medicine2_safe = self.config.medicine2.lower().replace(" ", "_")
        base_filename = f"{medicine1_safe}_vs_{medicine2_safe}_comparison"

        return save_model_response(result, output_dir / base_filename)
