"""
Clinical Sign Recognizer Agentic Module.

This module provides an agentic approach to clinical sign identification using the agno framework.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.clinical_sign_models import ClinicalSignIdentifierModel
from ..shared.clinical_sign_prompts import ClinicalSignInput, PromptBuilder


class ClinicalSignRecognizerAgent(BaseAgenticRecognizer):
    """Agentic clinical sign identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return ClinicalSignInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return ClinicalSignIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "sign_name"
