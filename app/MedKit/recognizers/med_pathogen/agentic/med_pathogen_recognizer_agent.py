"""
Medical Pathogen Recognizer Agentic Module.

This module provides an agentic approach to pathogen identification using the agno framework.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.med_pathogen_models import PathogenIdentifierModel
from ..shared.med_pathogen_prompts import PathogenIdentifierInput, PromptBuilder


class MedicalPathogenRecognizerAgent(BaseAgenticRecognizer):
    """Agentic pathogen identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return PathogenIdentifierInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return PathogenIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "pathogen_name"
