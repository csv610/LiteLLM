"""Specialized agents for medical speciality roles generation."""

import logging
from typing import Any, Callable, Type

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient

from .med_speciality_roles_models import (
    ModelOutput,
    SpecialityRoleInfo,
    ComplianceReviewModel,
)
from .med_speciality_roles_prompts import PromptBuilder

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
        """Execute the agent's task for the given topic."""
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


class SpecialityAgent(BaseAgent):
    """Agent for medical speciality roles and responsibilities."""

    def run(self, speciality: str, structured: bool) -> ModelOutput:
        return self.generate(
            speciality,
            structured,
            SpecialityRoleInfo,
            PromptBuilder.create_speciality_agent_prompts,
        )


class ComplianceAgent(BaseAgent):
    """Agent for final compliance and regulatory review (Outputs JSON)."""

    def run(self, speciality: str, content: str, structured: bool) -> ModelOutput:
        """Run the compliance review on the provided content and return structured JSON."""
        system_prompt, user_prompt = PromptBuilder.create_compliance_agent_prompts(
            speciality, content
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

    def run(self, speciality: str, specialist_data: str, compliance_data: str) -> str:
        """Synthesize all inputs into a final, polished Markdown report."""
        system_prompt, user_prompt = PromptBuilder.create_output_agent_prompts(
            speciality, specialist_data, compliance_data
        )
        logger.debug("OutputAgent starting final synthesis (Markdown).")

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=None, # Always Markdown
        )

        try:
            res = self.client.generate_text(model_input=model_input)
            return res.markdown
        except Exception as e:
            logger.error(f"Error in OutputAgent: {e}")
            raise
