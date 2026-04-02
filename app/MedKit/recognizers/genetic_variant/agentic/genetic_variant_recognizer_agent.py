"""
Genetic Variant Recognizer Agentic Module.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel

from ...base_agentic_recognizer import BaseAgenticRecognizer
from ..shared.genetic_variant_models import GeneticVariantIdentifierModel
from ..shared.genetic_variant_prompts import GeneticVariantInput, PromptBuilder


class GeneticVariantRecognizerAgent(BaseAgenticRecognizer):
    """Agentic genetic variant identifier using agno framework."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_system_prompt()

    def get_input_class(self) -> Type[BaseModel]:
        return GeneticVariantInput

    def get_response_model(self) -> Optional[Type[BaseModel]]:
        return GeneticVariantIdentifierModel

    def _get_prompt_builder(self) -> Type[Any]:
        return PromptBuilder

    def _get_name_field(self) -> str:
        return "variant_name"
