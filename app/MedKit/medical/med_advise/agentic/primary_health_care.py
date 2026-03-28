#!/usr/bin/env python3
"""
Primary Health Care module.

This module provides the PrimaryHealthCareProvider class for addressing
patient questions with a multi-agentic perspective.
"""

import logging
from pathlib import Path
from typing import Optional

from lite.config import ModelConfig
from lite.utils import save_model_response

from .primary_health_care_agents import (
    TriageAgent,
    EducatorAgent,
    AdvisorAgent,
    ClinicalAgent,
)
from .primary_health_care_models import ModelOutput, PrimaryCareResponseModel

logger = logging.getLogger(__name__)


class PrimaryHealthCareProvider:
    """Orchestrates multiple agents to provide general medical information."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.triage_agent = TriageAgent(model_config)
        self.educator_agent = EducatorAgent(model_config)
        self.advisor_agent = AdvisorAgent(model_config)
        self.clinical_agent = ClinicalAgent(model_config)
        self.query = None
        logger.debug("Initialized Multi-Agent PrimaryHealthCareProvider")

    def generate_text(self, query: str, structured: bool = False) -> ModelOutput:
        """Orchestrates agents to address a patient's health concern."""
        if not query or not str(query).strip():
            raise ValueError("Query cannot be empty")

        self.query = query
        logger.info(f"Addressing health concern: {query}")

        # 1. Triage the concern
        triage_data = self.triage_agent.process(query)
        context = (
            f"Understanding Concern: {triage_data.understanding_concern}\n"
            f"Symptoms: {', '.join(triage_data.common_symptoms)}"
        )

        # 2. Get Medical Education
        education_data = self.educator_agent.process(query, context)

        # 3. Get Self-Care Advice
        advisor_data = self.advisor_agent.process(query, context)

        # 4. Get Clinical Guidance
        clinical_data = self.clinical_agent.process(query, context)

        # Synthesis
        synthesized_data = PrimaryCareResponseModel(
            understanding_concern=triage_data.understanding_concern,
            common_symptoms=triage_data.common_symptoms,
            general_explanation=education_data.general_explanation,
            self_care_advice=advisor_data.self_care_advice,
            when_to_seek_care=clinical_data.when_to_seek_care,
            next_steps=clinical_data.next_steps,
        )

        markdown_output = self._format_markdown(synthesized_data)

        return ModelOutput(
            data=synthesized_data if structured else None, markdown=markdown_output
        )

    def _format_markdown(self, data: PrimaryCareResponseModel) -> str:
        """Formats the synthesized response into markdown."""
        sections = [
            f"# Understanding Your Concern\n{data.understanding_concern}",
            f"# Common Symptoms and Observations\n"
            + "\n".join([f"- {s}" for s in data.common_symptoms]),
            f"# General Explanation\n{data.general_explanation}",
            f"# General Advice and Self-Care\n{data.self_care_advice}",
            f"# When to Seek Medical Attention\n{data.when_to_seek_care}",
            f"# Next Steps\n" + "\n".join([f"- {s}" for s in data.next_steps]),
        ]
        return "\n\n".join(sections)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the provider's response to a file."""
        if self.query is None:
            raise ValueError("No query information available.")

        safe_query = "".join(
            [c if c.isalnum() else "_" for c in self.query[:30].lower()]
        ).strip("_")
        base_filename = f"response_{safe_query}"

        return save_model_response(result, output_dir / base_filename)
