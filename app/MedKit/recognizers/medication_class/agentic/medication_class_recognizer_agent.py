"""
Medication Class Recognizer Agentic Module.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.medication_class_models import MedicationClassIdentifierModel
from ..shared.medication_class_prompts import (
    MedicationClassIdentifierInput,
    PromptBuilder,
)


class MedicationClassRecognizerAgent(BaseAgenticRecognizer):
    """Agentic medication class identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return MedicationClassIdentifierInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return MedicationClassIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "class_name"
