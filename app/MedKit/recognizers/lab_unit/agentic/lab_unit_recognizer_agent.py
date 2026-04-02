"""
Lab Unit Recognizer Agentic Module.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.lab_unit_models import LabUnitIdentifierModel
from ..shared.lab_unit_prompts import LabUnitInput, PromptBuilder


class LabUnitRecognizerAgent(BaseAgenticRecognizer):
    """Agentic lab unit identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return LabUnitInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return LabUnitIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "unit_name"
