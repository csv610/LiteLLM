"""
Medical Abbreviation Recognizer Agentic Module.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.med_abbreviation_models import AbbreviationIdentifierModel
from ..shared.med_abbreviation_prompts import (
    AbbreviationIdentifierInput,
    PromptBuilder,
)


class MedicalAbbreviationRecognizerAgent(BaseAgenticRecognizer):
    """Agentic medical abbreviation identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return AbbreviationIdentifierInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return AbbreviationIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "abbreviation"
