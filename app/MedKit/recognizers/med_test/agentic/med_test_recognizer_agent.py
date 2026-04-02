"""
Medical Test Recognizer Agentic Module.

This module provides an agentic approach to medical test identification using the agno framework.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.med_test_models import MedicalTestIdentifierModel
from ..shared.med_test_prompts import MedicalTestIdentifierInput, PromptBuilder


class MedicalTestRecognizerAgent(BaseAgenticRecognizer):
    """Agentic medical test identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return MedicalTestIdentifierInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return MedicalTestIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "test_name"
