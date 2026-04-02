"""
Medical Vaccine Recognizer Agentic Module.

This module provides an agentic approach to vaccine identification using the agno framework.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.med_vaccine_models import VaccineIdentifierModel
from ..shared.med_vaccine_prompts import VaccineIdentifierInput, PromptBuilder


class MedicalVaccineRecognizerAgent(BaseAgenticRecognizer):
    """Agentic vaccine identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return VaccineIdentifierInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return VaccineIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "vaccine_name"
