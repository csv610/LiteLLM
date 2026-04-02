"""
Medical Device Recognizer Agentic Module.

This module provides an agentic approach to medical device identification using the agno framework.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.med_device_models import MedicalDeviceIdentifierModel
from ..shared.med_device_prompts import MedicalDeviceIdentifierInput, PromptBuilder


class MedicalDeviceRecognizerAgent(BaseAgenticRecognizer):
    """Agentic medical device identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return MedicalDeviceIdentifierInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return MedicalDeviceIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "device_name"
