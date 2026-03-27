#!/usr/bin/env python3
"""
Drug Addiction Analysis module.

This module provides the core DrugAddiction class for analyzing
the addictive potential and risks associated with medicines and substances.
"""

import logging
from pathlib import Path
from typing import Optional, Union

from drug_addiction_models import (
    DrugAddictionModel,
    ModelOutput,
    WithdrawalSymptomModel,
)
from drug_addiction_prompts import DrugAddictionInput, PromptBuilder
from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

logger = logging.getLogger(__name__)


class DrugAddiction:
    """Analyzes drug addiction risks based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the drug addiction analyzer."""
        self.client = LiteClient(model_config)
        self.config: Optional[DrugAddictionInput] = None
        logger.debug("Initialized DrugAddiction")

    def generate_text(self, config: DrugAddictionInput) -> ModelOutput:
        """Analyze addiction risks and return structured data plus rendered markdown."""
        # Store the configuration for later use in save
        self.config = config
        logger.debug("Starting drug addiction analysis")
        logger.debug(f"Substance: {config.medicine_name}")

        # Create user prompt with context
        user_prompt = PromptBuilder.create_user_prompt(config)
        system_prompt = PromptBuilder.create_system_prompt()
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=DrugAddictionModel,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            raw_result = self._ask_llm(model_input)
            result = ModelOutput(
                data=raw_result, markdown=self._render_markdown(raw_result)
            )
            logger.debug("✓ Successfully analyzed addiction risks")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating drug addiction analysis: {e}")
            raise

    def generate_markdown(self, config: DrugAddictionInput) -> ModelOutput:
        """Analyze addiction risks and return markdown directly from the model."""
        self.config = config
        logger.debug("Starting markdown-only drug addiction analysis")

        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(config),
            response_format=None,
        )

        raw_result = self._ask_llm(model_input)
        if not isinstance(raw_result, str):
            raise TypeError(
                "Expected markdown string from LiteClient when response_format is None."
            )
        return ModelOutput(markdown=raw_result)

    def _ask_llm(self, model_input: ModelInput) -> Union[DrugAddictionModel, str]:
        """Helper to call LiteClient with error handling."""
        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"✗ Error during LLM analysis: {e}")
            logger.exception("Full exception details:")
            raise

    def _render_markdown(self, result: DrugAddictionModel) -> str:
        """Render a readable markdown report from structured output."""
        lines = ["# Drug Addiction Analysis", ""]

        details = result.addiction_details
        if details is not None:
            lines.extend(
                [
                    f"## {details.medicine_name}",
                    "",
                    f"- Addiction potential: {details.addiction_potential.value}",
                    f"- Confidence level: {details.confidence_level.value}",
                ]
            )
            if details.dea_schedule is not None:
                lines.append(f"- DEA schedule: {details.dea_schedule.value}")
            if details.other_names:
                lines.append(f"- Other names: {', '.join(details.other_names)}")
            lines.append("")
            lines.extend(
                [
                    "### Mechanism",
                    "",
                    f"- Neurotransmitter impact: {details.mechanism.neurotransmitter_impact}",
                    f"- Psychological factors: {details.mechanism.psychological_factors}",
                    f"- Physiological dependence: {details.mechanism.physiological_dependence}",
                    "",
                ]
            )
            lines.extend(
                self._render_bullets(
                    "Withdrawal Symptoms",
                    [
                        self._format_withdrawal_symptom(symptom)
                        for symptom in details.withdrawal_symptoms
                    ],
                )
            )
            lines.extend(
                self._render_bullets("Long-term Effects", details.long_term_effects)
            )
            lines.extend(self._render_bullets("Risk Factors", details.risk_factors))
            lines.extend(
                self._render_bullets("Treatment Options", details.treatment_options)
            )
            lines.extend(
                self._render_bullets(
                    "Prevention Strategies", details.prevention_strategies
                )
            )
            if details.references:
                lines.extend(["### References", "", details.references, ""])

        lines.extend(["## Technical Summary", "", result.technical_summary, ""])

        if result.patient_friendly_summary is not None:
            patient = result.patient_friendly_summary
            lines.extend(["## Patient-Friendly Summary", "", patient.simple_explanation, ""])
            lines.extend(
                self._render_bullets("Signs of Addiction", patient.signs_of_addiction)
            )
            lines.extend(["### What To Do", "", patient.what_to_do, ""])
            lines.extend(["### Recovery Outlook", "", patient.recovery_outlook, ""])

        return "\n".join(lines).strip() + "\n"

    def _render_bullets(self, heading: str, items: list[str]) -> list[str]:
        """Render a markdown heading with a bullet list."""
        lines = [f"### {heading}", ""]
        if items:
            lines.extend(f"- {item}" for item in items)
        else:
            lines.append("- Not provided")
        lines.append("")
        return lines

    def _format_withdrawal_symptom(self, symptom: WithdrawalSymptomModel) -> str:
        """Format a withdrawal symptom for markdown output."""
        parts = [f"{symptom.symptom} ({symptom.severity.value})"]
        if symptom.duration:
            parts.append(f"duration: {symptom.duration}")
        if symptom.management:
            parts.append(f"management: {symptom.management}")
        return "; ".join(parts)

    def save_markdown(self, result: ModelOutput, output_dir: Path) -> Path:
        """Save markdown output to disk."""
        if self.config is None:
            raise ValueError("No configuration available. Call generate_text first.")
        if not result.markdown:
            raise ValueError("No markdown content available to save.")

        base_filename = f"{self.config.medicine_name.lower().replace(' ', '_')}"
        return save_model_response(result.markdown, output_dir / base_filename)

    def save_structured(self, result: ModelOutput, output_dir: Path) -> Path:
        """Save structured JSON output to disk."""
        if self.config is None:
            raise ValueError("No configuration available. Call generate_text first.")
        if result.data is None:
            raise ValueError("No structured data available to save.")

        base_filename = f"{self.config.medicine_name.lower().replace(' ', '_')}"
        return save_model_response(result.data, output_dir / base_filename)

    def save(
        self, result: ModelOutput, output_dir: Path, include_structured: bool = True
    ) -> Path:
        """Save markdown and optionally save a structured JSON sidecar."""
        markdown_path = self.save_markdown(result, output_dir)
        if include_structured and result.data is not None:
            self.save_structured(result, output_dir)
        return markdown_path
