#!/usr/bin/env python3
"""
Medical FAQ Analysis module.

This module provides the core MedicalFAQGenerator class for generating
comprehensive FAQ content for medical topics using a multi-agentic approach
with a final compliance validation step.
"""

import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.utils import save_model_response

from .medical_agents import (
    ClinicalAgent,
    ComplianceAgent,
    OutputAgent,
    PatientAgent,
    ResearchAgent,
    SafetyAgent,
)
from .medical_faq_models import MedicalFAQModel, ModelOutput, PatientFAQModel

logger = logging.getLogger(__name__)


class MedicalFAQGenerator:
    """Generates comprehensive FAQ content using a 3-tier multi-agent approach."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the FAQ generator with specialized agents."""
        self.model_config = model_config
        self.patient_agent = PatientAgent(model_config)
        self.clinical_agent = ClinicalAgent(model_config)
        self.safety_agent = SafetyAgent(model_config)
        self.research_agent = ResearchAgent(model_config)
        self.compliance_agent = ComplianceAgent(model_config)
        self.output_agent = OutputAgent(model_config)
        self.topic = None  # Store the topic for later use in save
        logger.debug("Initialized 3-tier MedicalFAQGenerator")

    def generate_text(self, topic: str, structured: bool = False) -> ModelOutput:
        """Generate comprehensive FAQ content using a 3-tier agent system.

        Args:
            topic: Medical topic for FAQ generation
            structured: Whether to use structured output (Pydantic models)

        Returns:
            ModelOutput: Aggregated and synthesized result
        """
        if not topic or not str(topic).strip():
            raise ValueError("Topic name cannot be empty")

        self.topic = topic
        logger.info(f"Starting 3-tier FAQ generation for: {topic}")

        try:
            # 1. Run Specialist agents
            logger.debug("Running Specialist agents...")
            patient_res = self.patient_agent.run(topic, structured)
            clinical_res = self.clinical_agent.run(topic, structured)
            safety_res = self.safety_agent.run(topic, structured)
            research_res = self.research_agent.run(topic, structured)

            # Preliminary Aggregation
            if structured:
                aggregated = self._aggregate_structured(
                    patient_res, clinical_res, safety_res, research_res
                )
                spec_content = aggregated.data.model_dump_json(indent=2)
            else:
                aggregated = self._aggregate_unstructured(
                    patient_res, clinical_res, safety_res, research_res
                )
                spec_content = aggregated.markdown

            # 2. Compliance Audit Stage (JSON/Audit)
            logger.debug("Running ComplianceAgent audit...")
            compliance_res = self.compliance_agent.run(
                topic, spec_content, structured
            )
            # Handle compliance_res being ModelOutput or direct data
            comp_content = (
                compliance_res.data.model_dump_json(indent=2)
                if hasattr(compliance_res, 'data') and compliance_res.data 
                else str(compliance_res)
            )

            # 3. Final Synthesis Stage (Markdown/Refinement)
            logger.debug("Running OutputAgent final synthesis...")
            final_markdown = self.output_agent.run(
                topic, spec_content, comp_content
            )

            return ModelOutput(
                data=aggregated.data if structured else None,
                markdown=final_markdown,
                metadata={"audit": comp_content}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier generation failed: {e}")
            raise

    def _aggregate_structured(
        self,
        patient_res: ModelOutput,
        clinical_res: ModelOutput,
        safety_res: ModelOutput,
        research_res: ModelOutput,
    ) -> ModelOutput:
        """Combine structured data from generation agents."""
        patient_info = patient_res.data
        clinical_info = clinical_res.data
        safety_info = safety_res.data
        research_info = research_res.data

        patient_faq = PatientFAQModel(
            topic_name=self.topic,
            introduction=patient_info.introduction,
            faqs=patient_info.faqs,
            when_to_seek_care=safety_info.when_to_seek_care,
            misconceptions=safety_info.misconceptions,
            see_also=research_info.see_also,
        )

        medical_faq = MedicalFAQModel(
            topic_name=self.topic,
            metadata={"source": "multi-agentic-system"},
            patient_faq=patient_faq,
            provider_faq=clinical_info,
        )

        return ModelOutput(data=medical_faq)

    def _aggregate_unstructured(
        self,
        patient_res: ModelOutput,
        clinical_res: ModelOutput,
        safety_res: ModelOutput,
        research_res: ModelOutput,
    ) -> ModelOutput:
        """Combine markdown content from generation agents."""
        combined_md = [
            f"# Medical FAQ: {self.topic}",
            "## Patient Information",
            patient_res.markdown,
            "## Safety & Triage Guidance",
            safety_res.markdown,
            "## Related Topics & Research",
            research_res.markdown,
            "## Clinical Overview for Providers",
            clinical_res.markdown,
        ]

        return ModelOutput(markdown="\n\n".join(combined_md))

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical FAQ information to a file."""
        if self.topic is None:
            raise ValueError(
                "No topic information available. Call generate_text first."
            )

        base_filename = f"{self.topic.lower().replace(' ', '_')}_faq_agentic"
        return save_model_response(result, output_dir / base_filename)
