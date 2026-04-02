"""
Medical Supplement Recognizer Agentic Module.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.med_supplement_models import SupplementIdentifierModel
from ..shared.med_supplement_prompts import SupplementIdentifierInput, PromptBuilder


class MedicalSupplementRecognizerAgent(BaseAgenticRecognizer):
    """Agentic medical supplement identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return SupplementIdentifierInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return SupplementIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "supplement_name"
