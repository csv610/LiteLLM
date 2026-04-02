"""
Medical Coding Recognizer Agentic Module.

This module provides an agentic approach to medical coding identification using the agno framework.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.med_coding_models import MedicalCodingIdentifierModel
from ..shared.med_coding_prompts import MedicalCodingInput, PromptBuilder


class MedicalCodingRecognizerAgent(BaseAgenticRecognizer):
    """Agentic medical coding identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return MedicalCodingInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return MedicalCodingIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "system_name"
