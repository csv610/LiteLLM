"""
Medical Symptom Recognizer Agentic Module.

This module provides an agentic approach to symptom identification using the agno framework.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.med_symptom_models import MedicalSymptomIdentifierModel
from ..shared.med_symptom_prompts import MedicalSymptomIdentifierInput, PromptBuilder


class MedicalSymptomRecognizerAgent(BaseAgenticRecognizer):
    """Agentic symptom identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return MedicalSymptomIdentifierInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return MedicalSymptomIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "symptom_name"
