"""Specialized agents for primary health care."""

import logging
from typing import Any, Type

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient

from .primary_health_care_models import (
    TriageResponseModel,
    EducationResponseModel,
    SelfCareResponseModel,
    ClinicalResponseModel,
)
from .primary_health_care_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for primary care agents."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)

    def _generate(
        self,
        query: str,
        system_prompt: str,
        response_format: Type[Any],
        context: str = "",
    ) -> Any:
        user_prompt = PromptBuilder.create_user_prompt(query, context)
        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )
        result = self.client.generate_text(model_input=model_input)
        return result.data


class TriageAgent(BaseAgent):
    """Agent specialized in understanding the user's health concern."""

    def process(self, query: str) -> TriageResponseModel:
        logger.debug("TriageAgent: Processing query...")
        return self._generate(
            query, PromptBuilder.create_triage_system_prompt(), TriageResponseModel
        )


class EducatorAgent(BaseAgent):
    """Agent specialized in providing medical explanations."""

    def process(self, query: str, context: str) -> EducationResponseModel:
        logger.debug("EducatorAgent: Providing medical background...")
        return self._generate(
            query,
            PromptBuilder.create_education_system_prompt(),
            EducationResponseModel,
            context,
        )


class AdvisorAgent(BaseAgent):
    """Agent specialized in practical self-care advice."""

    def process(self, query: str, context: str) -> SelfCareResponseModel:
        logger.debug("AdvisorAgent: Offering self-care advice...")
        return self._generate(
            query,
            PromptBuilder.create_advisor_system_prompt(),
            SelfCareResponseModel,
            context,
        )


class ClinicalAgent(BaseAgent):
    """Agent specialized in clinical guidance and red flags."""

    def process(self, query: str, context: str) -> ClinicalResponseModel:
        logger.debug("ClinicalAgent: Defining clinical red flags...")
        return self._generate(
            query,
            PromptBuilder.create_clinical_system_prompt(),
            ClinicalResponseModel,
            context,
        )
