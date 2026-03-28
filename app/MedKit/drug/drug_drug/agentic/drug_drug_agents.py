"""
drug_drug_agents.py - Specialized agents for drug-drug interaction analysis.
"""

import logging
from typing import Type, TypeVar

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from pydantic import BaseModel

try:
    from .drug_drug_interaction_models import (
        DrugInteractionDetailsModel,
        PatientFriendlySummaryModel,
    )
    from .drug_drug_interaction_prompts import DrugDrugInput, DrugDrugPromptBuilder
except ImportError:
    from drug_drug_interaction_models import (
        DrugInteractionDetailsModel,
        PatientFriendlySummaryModel,
    )
    from drug_drug_interaction_prompts import DrugDrugInput, DrugDrugPromptBuilder

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class BaseAgent:
    """Base class for specialized drug-drug interaction agents."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)

    def run(self, user_input: DrugDrugInput, response_format: Type[T]) -> T:
        """Run the agent with the given input and expected response format."""
        system_prompt = self.get_system_prompt()
        user_prompt = DrugDrugPromptBuilder.create_user_prompt(user_input)

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug(f"Running {self.__class__.__name__}...")
        return self.client.generate_text(model_input=model_input)

    async def run_async(
        self,
        user_input: DrugDrugInput,
        response_format: Type[T],
        custom_user_prompt: str | None = None,
    ) -> T:
        """Run the agent asynchronously with the given input."""
        system_prompt = self.get_system_prompt()
        user_prompt = (
            custom_user_prompt
            if custom_user_prompt
            else DrugDrugPromptBuilder.create_user_prompt(user_input)
        )

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug(f"Running {self.__class__.__name__} (async)...")
        # Assuming LiteClient.generate_text has an async version or can be run in a thread
        # For now, we'll wrap it in a thread if no async version exists
        import asyncio
        from functools import partial

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, partial(self.client.generate_text, model_input=model_input)
        )

    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent. Must be overridden."""
        raise NotImplementedError


class TriageAgent(BaseAgent):
    """Agent specializing in initial triage of interactions."""

    def get_system_prompt(self) -> str:
        return DrugDrugPromptBuilder.create_triage_system_prompt()


class PharmacologyAgent(BaseAgent):
    """Agent specializing in pharmacological mechanisms."""

    def get_system_prompt(self) -> str:
        return DrugDrugPromptBuilder.create_pharmacology_system_prompt()


class RiskAssessmentAgent(BaseAgent):
    """Agent specializing in clinical risk assessment."""

    def get_system_prompt(self) -> str:
        return DrugDrugPromptBuilder.create_risk_assessment_system_prompt()


class ManagementAgent(BaseAgent):
    """Agent specializing in clinical management recommendations."""

    def get_system_prompt(self) -> str:
        return DrugDrugPromptBuilder.create_management_system_prompt()


class PatientEducationAgent(BaseAgent):
    """Agent specializing in patient-friendly communication."""

    def get_system_prompt(self) -> str:
        return DrugDrugPromptBuilder.create_patient_education_system_prompt()


class SearchAgent(BaseAgent):
    """Agent specializing in medical evidence research."""

    def get_system_prompt(self) -> str:
        return DrugDrugPromptBuilder.create_search_agent_system_prompt()


class ComplianceAgent(BaseAgent):
    """Agent specializing in medical compliance and safety review."""

    def get_system_prompt(self) -> str:
        return DrugDrugPromptBuilder.create_compliance_system_prompt()
