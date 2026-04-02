"""
Disease Recognizer Agentic Module.

This module provides an agentic approach to disease identification using the agno framework.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.disease_identifier_models import DiseaseIdentifierModel
from ..shared.disease_identifier_prompts import DiseaseIdentifierInput, PromptBuilder


class DiseaseRecognizerAgent(BaseAgenticRecognizer):
    """Agentic disease identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return DiseaseIdentifierInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return DiseaseIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "disease_name"
