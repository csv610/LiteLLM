"""
Medical Anatomy Recognizer Agentic Module.

This module provides an agentic approach to anatomy identification using the agno framework.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.med_anatomy_identifier_models import MedicalAnatomyIdentifierModel
from ..shared.med_anatomy_identifier_prompts import (
    MedicalAnatomyIdentifierInput,
    PromptBuilder,
)


class MedicalAnatomyRecognizerAgent(BaseAgenticRecognizer):
    """Agentic anatomy identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return MedicalAnatomyIdentifierInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return MedicalAnatomyIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "structure_name"
