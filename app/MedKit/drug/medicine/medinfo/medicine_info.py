"""Medicine Information Generator.

This module contains the core logic for generating comprehensive medicine information
using AI-powered analysis.
"""

import logging
from pathlib import Path
from typing import Union

from lite.config import ModelConfig, ModelInput
from lite.llm_client import LiteClient

from medicine_info_models import MedicineInfoModel, ModelOutput
from medicine_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicineInfoGenerator:
    """Generates comprehensive medicine information."""

    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)
        self.logger = logging.getLogger(__name__)

    def generate_text( self, medicine_name: str, structured: bool = False) -> ModelOutput:
        """Generate comprehensive medicine information.

        Args:
            medicine_name: Name of the medicine
            structured: Whether to use structured output (Pydantic model)

        Returns:
            Union[MedicineInfoResult, str]: Structured or plain text result
        """
        if not medicine_name or not medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")

        self.logger.debug(f"Starting medicine information fetch for: {medicine_name}")

        # Create model input with prompts
        user_prompt = PromptBuilder.create_user_prompt(medicine_name)
        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=user_prompt,
            response_format=MedicineInfoModel if structured else None,
        )

        result = self.client.generate_text(model_input=model_input)
        self.logger.debug(f"✓ Successfully fetched info for {medicine_name}")
        return result

    def save(self, result: ModelOutput, str], output_path: Path) -> Path:
        """Save the generated information to a file."""
        from lite.utils import save_model_response
        return save_model_response(result, output_path)
