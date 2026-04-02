"""
Drug Recognizer Agentic Module.

This module provides an agentic approach to drug identification using the agno framework.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.drug_recognizer_model import DrugIdentifierModel
from ..shared.drug_recognizer_prompts import DrugIdentifierInput, PromptBuilder


class DrugRecognizerAgent(BaseAgenticRecognizer):
    """Agentic drug identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return DrugIdentifierInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return DrugIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "drug_name"
