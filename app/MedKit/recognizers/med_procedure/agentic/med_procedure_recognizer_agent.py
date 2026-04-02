"""
Medical Procedure Recognizer Agentic Module.

This module provides an agentic approach to medical procedure identification using the agno framework.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.med_procedure_models import MedicalProcedureIdentifierModel
from ..shared.med_procedure_prompts import (
    MedicalProcedureIdentifierInput,
    PromptBuilder,
)


class MedicalProcedureRecognizerAgent(BaseAgenticRecognizer):
    """Agentic medical procedure identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return MedicalProcedureIdentifierInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return MedicalProcedureIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "procedure_name"
