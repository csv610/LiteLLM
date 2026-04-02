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
        """Addresses health concern using a 3-tier multi-agent system."""
        if not query or not str(query).strip():
            raise ValueError("Query cannot be empty")

        self.query = query
        logger.info(f"Addressing 3-tier health concern: {query}")

        try:
            # 1. Specialist Stage (JSON)
            logger.debug("Tier 1: Specialists processing concern...")
            triage_data = self.triage_agent.process(query)
            context = (
                f"Understanding Concern: {triage_data.understanding_concern}\n"
                f"Symptoms: {', '.join(triage_data.common_symptoms)}"
            )
            education_data = self.educator_agent.process(query, context)
            advisor_data = self.advisor_agent.process(query, context)
            clinical_data = self.clinical_agent.process(query, context)

            spec_data = PrimaryCareResponseModel(
                understanding_concern=triage_data.understanding_concern,
                common_symptoms=triage_data.common_symptoms,
                general_explanation=education_data.general_explanation,
                self_care_advice=advisor_data.self_care_advice,
                when_to_seek_care=clinical_data.when_to_seek_care,
                next_steps=clinical_data.next_steps,
            )
            spec_json = spec_data.model_dump_json(indent=2)

            # 2. Auditor Stage (JSON Audit)
            logger.debug("Tier 2: Auditor checking safety...")
            audit_sys, audit_usr = PromptBuilder.get_compliance_auditor_prompts(query, spec_json)
            audit_input = ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None # Audit result
            )
            audit_res = self.advisor_agent.client.generate_text(model_input=audit_input)
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown)
            logger.debug("Tier 3: Output Agent synthesizing final response...")
            out_sys, out_usr = PromptBuilder.get_output_synthesis_prompts(query, spec_json, audit_json)
            out_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.advisor_agent.client.generate_text(model_input=out_input)

            logger.info("✓ Successfully generated 3-tier health advice")
            return ModelOutput(
                data=spec_data if structured else None, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier advice generation failed: {e}")
            raise

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
