"""
Imaging Finding Recognizer Agentic Module.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.imaging_finding_models import ImagingFindingIdentifierModel
from ..shared.imaging_finding_prompts import ImagingFindingInput, PromptBuilder


class ImagingFindingRecognizerAgent(BaseAgenticRecognizer):
    """Agentic imaging finding identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return ImagingFindingInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return ImagingFindingIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "finding_name"
