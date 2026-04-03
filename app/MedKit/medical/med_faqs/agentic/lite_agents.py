"""
liteagents.py - Unified for med_faqs
"""
from lite.utils import save_model_response
from typing import Any, Callable, Type
from .medical_faq_prompts import PromptBuilder
from tqdm import tqdm
from app.MedKit.medical.med_faqs.shared.models import *
import pytest
import logging
from .medical_faq_models import (
from lite.lite_client import LiteClient
from pathlib import Path
from .medical_agents import (
import argparse
from lite.config import ModelConfig, ModelInput
from unittest.mock import patch, MagicMock
from lite.logging_config import configure_logging
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


# Corrected import for the agentic version
    ModelOutput,
    MedicalFAQModel,
    PatientBasicInfoModel,
    ProviderFAQModel,
    SafetyInfoModel,
    ResearchInfoModel,
    ComplianceReviewModel,
    FAQItemModel,
    PatientFAQModel,
)


@pytest.fixture
def mock_lite_client():
    # Mock the LiteClient in the medical_agents module
    with patch("medical.med_faqs.agentic.medical_agents.LiteClient") as mock:
        yield mock


def test_medical_faq_generator_init():
    config = ModelConfig(model="test-model")
    generator = MedicalFAQGenerator(config)
    assert generator.model_config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalFAQGenerator(config)

    # We need to provide a mock response for each of the 5 agents (including Compliance)
    mock_instance = mock_lite_client.return_value
    mock_instance.generate_text.side_effect = [
        ModelOutput(markdown="Patient info"),
        ModelOutput(markdown="Clinical info"),
        ModelOutput(markdown="Safety info"),
        ModelOutput(markdown="Research info"),
        ModelOutput(markdown="Compliance: All clear."),
    ]

    result = generator.generate_text("What is diabetes?", structured=False)
    assert "Patient info" in result.markdown
    assert "Clinical info" in result.markdown
    assert "Safety info" in result.markdown
    assert "Research info" in result.markdown
    assert "Compliance: All clear." in result.markdown


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalFAQGenerator(config)

    # We need to provide structured mock data for each agent
    mock_instance = mock_lite_client.return_value

    # 1. PatientAgent
    patient_info = PatientBasicInfoModel(
        introduction="Intro",
        faqs=[FAQItemModel(question="Q1", answer="A1")]
    )
    # 2. ClinicalAgent
    clinical_info = ProviderFAQModel(
        topic_name="Diabetes",
        clinical_overview="Overview",
        clinical_faqs=[],
        evidence_based_practices=[],
        quality_metrics=[],
        referral_criteria=[]
    )
    # 3. SafetyAgent
    safety_info = SafetyInfoModel(
        when_to_seek_care=[],
        misconceptions=[]
    )
    # 4. ResearchAgent
    research_info = ResearchInfoModel(
        see_also=[]
    )
    # 5. ComplianceAgent
    compliance_info = ComplianceReviewModel(
        is_compliant=True,
        issues_found=[],
        required_disclaimers=["Mandatory disclaimer"],
        suggested_edits=None
    )

    mock_instance.generate_text.side_effect = [
        ModelOutput(data=patient_info),
        ModelOutput(data=clinical_info),
        ModelOutput(data=safety_info),
        ModelOutput(data=research_info),
        ModelOutput(data=compliance_info),
    ]

    result = generator.generate_text("What is diabetes?", structured=True)
    assert result.data.topic_name == "What is diabetes?"
    assert result.data.patient_faq.introduction == "Intro"
    assert result.data.compliance_review.is_compliant is True
    assert "Mandatory disclaimer" in result.data.compliance_review.required_disclaimers

#!/usr/bin/env python3
"""
Medical FAQ Analysis module.

This module provides the core MedicalFAQGenerator class for generating
comprehensive FAQ content for medical topics using a multi-agentic approach
with a final compliance validation step.
"""



    ClinicalAgent,
    ComplianceAgent,
    OutputAgent,
    PatientAgent,
    ResearchAgent,
    SafetyAgent,
)

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

        return ModelOutput(markdown="

".join(combined_md))

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical FAQ information to a file."""
        if self.topic is None:
            raise ValueError(
                "No topic information available. Call generate_text first."
            )

        base_filename = f"{self.topic.lower().replace(' ', '_')}_faq_agentic"
        return save_model_response(result, output_dir / base_filename)

"""Medical FAQ Generator CLI."""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))




try:
    from .medical_faq import MedicalFAQGenerator
except (ImportError, ValueError):
    from medical.med_faqs.agentic.medical_faq import MedicalFAQGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate comprehensive medical FAQs.")
    parser.add_argument("topic", help="Medical topic or file path containing topics.")
    parser.add_argument(
        "-d", "--output-dir", default="outputs", help="Output directory."
    )
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Verbosity level.",
    )
    parser.add_argument(
        "-s", "--structured", action="store_true", help="Use structured output."
    )
    return parser.parse_args()


def main():
    args = get_user_arguments()
    configure_logging(
        log_file="medical_faq.log", verbosity=args.verbosity, enable_console=True
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.topic)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.topic]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedicalFAQGenerator(model_config)

        for item in tqdm(items, desc="Generating"):
            result = generator.generate_text(topic=item, structured=args.structured)
            if result:
                generator.save(result, output_dir)

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())

"""Specialized agents for medical FAQ generation."""



    ModelOutput,
    PatientBasicInfoModel,
    ProviderFAQModel,
    ResearchInfoModel,
    SafetyInfoModel,
    ComplianceReviewModel,
)

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for specialized medical agents."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the agent with a model configuration."""
        self.model_config = model_config
        self.client = LiteClient(model_config)

    def generate(
        self,
        topic: str,
        structured: bool,
        response_format: Type[Any],
        prompts_fn: Callable[[str], tuple[str, str]],
    ) -> ModelOutput:
        """Execute the agent's task for the given topic.

        Args:
            topic: The medical topic.
            structured: Whether to use structured output.
            response_format: The Pydantic model for structured output.
            prompts_fn: Function that returns (system_prompt, user_prompt).

        Returns:
            ModelOutput: The agent's generated content.
        """
        system_prompt, user_prompt = prompts_fn(topic)
        logger.debug(f"Agent {self.__class__.__name__} starting generation.")

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format if structured else None,
        )

        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {e}")
            raise


class PatientAgent(BaseAgent):
    """Agent for patient-friendly FAQs and introductions."""

    def run(self, topic: str, structured: bool) -> ModelOutput:
        return self.generate(
            topic,
            structured,
            PatientBasicInfoModel,
            PromptBuilder.create_patient_agent_prompts,
        )


class ClinicalAgent(BaseAgent):
    """Agent for provider-focused clinical depth."""

    def run(self, topic: str, structured: bool) -> ModelOutput:
        return self.generate(
            topic,
            structured,
            ProviderFAQModel,
            PromptBuilder.create_clinical_agent_prompts,
        )


class SafetyAgent(BaseAgent):
    """Agent for safety guidance and debunking misconceptions."""

    def run(self, topic: str, structured: bool) -> ModelOutput:
        return self.generate(
            topic,
            structured,
            SafetyInfoModel,
            PromptBuilder.create_safety_agent_prompts,
        )


class ResearchAgent(BaseAgent):
    """Agent for identifying related topics, tests, and devices."""

    def run(self, topic: str, structured: bool) -> ModelOutput:
        return self.generate(
            topic,
            structured,
            ResearchInfoModel,
            PromptBuilder.create_research_agent_prompts,
        )


class ComplianceAgent(BaseAgent):
    """Agent for final compliance and regulatory review (Outputs JSON)."""

    def run(self, topic: str, content: str, structured: bool) -> ModelOutput:
        """Run the compliance review on the provided content and return structured JSON."""
        system_prompt, user_prompt = PromptBuilder.create_compliance_agent_prompts(
            topic, content
        )
        logger.debug("ComplianceAgent starting validation (JSON output).")

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=ComplianceReviewModel if structured else None,
        )

        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"Error in ComplianceAgent: {e}")
            raise


class OutputAgent(BaseAgent):
    """The Final Closer Agent. Synthesizes all specialists and compliance data into Markdown."""

    def run(self, topic: str, specialist_data: str, compliance_data: str) -> str:
        """Synthesize all inputs into a final, polished Markdown report."""
        system_prompt, user_prompt = PromptBuilder.create_output_agent_prompts(
            topic, specialist_data, compliance_data
        )
        logger.debug("OutputAgent starting final synthesis (Markdown).")

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=None, # Always Markdown for the absolute final stage
        )

        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"Error in OutputAgent: {e}")
            raise