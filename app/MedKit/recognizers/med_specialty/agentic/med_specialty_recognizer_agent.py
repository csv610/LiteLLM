"""
Medical Specialty Recognizer Agentic Module.

This module provides an agentic approach to medical specialty identification using the agno framework.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.med_specialty_models import MedicalSpecialtyIdentifierModel
from ..shared.med_specialty_prompts import (
    MedicalSpecialtyIdentifierInput,
    PromptBuilder,
)


class MedicalSpecialtyRecognizerAgent(BaseAgenticRecognizer):
    """Agentic medical specialty identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return MedicalSpecialtyIdentifierInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return MedicalSpecialtyIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "specialty_name"
