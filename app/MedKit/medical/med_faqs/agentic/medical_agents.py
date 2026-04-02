"""Specialized agents for medical FAQ generation."""

import logging
from typing import Any, Callable, Type

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient

from .medical_faq_models import (
    ModelOutput,
    PatientBasicInfoModel,
    ProviderFAQModel,
    ResearchInfoModel,
    SafetyInfoModel,
    ComplianceReviewModel,
)
from .medical_faq_prompts import PromptBuilder

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
