"""
Medical Condition Recognizer Agentic Module.

This module provides an agentic approach to medical condition identification using the agno framework.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.med_condition_models import MedicalConditionIdentifierModel
from ..shared.med_condition_prompts import (
    MedicalConditionIdentifierInput,
    PromptBuilder,
)


class MedicalConditionRecognizerAgent(BaseAgenticRecognizer):
    """Agentic medical condition identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return MedicalConditionIdentifierInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return MedicalConditionIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "condition_name"
