#!/usr/bin/env python3
"""
Medical Myths Checker module.

This module provides the core MedicalMythsChecker class for analyzing
medical myths for factual accuracy based on peer-reviewed evidence.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, List, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from medical_myth_checker_models import MedicalMythAnalysisModel, ModelOutput
from medical_myth_checker_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalMythsChecker:
    """Analyzes medical myths for factual accuracy based on peer-reviewed evidence."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the myths checker."""
        self.client = LiteClient(model_config=model_config)
        self.myth: Optional[str] = None

    def generate_text(self, myth: str, structured: bool = False) -> ModelOutput:
        """
        Analyze a medical myth and determine its status.

        Args:
            myth: The myth/claim to analyze.

        Returns:
            The generated MythAnalysisResponse object.

        Raises:
            ValueError: If myth is empty.
        """
        if not myth or not myth.strip():
            raise ValueError("Myth statement cannot be empty")

        self.myth = myth
        logger.debug(f"Starting medical myth analysis for: {myth}")

        response_format = None
        if structured:
            response_format = MedicalMythAnalysisModel

        model_input = ModelInput(
            system_prompt=PromptBuilder.system_prompt(),
            user_prompt=PromptBuilder.user_prompt(myth),
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        result = self._ask_llm(model_input)
        logger.debug("✓ Successfully analyzed medical myth")
        return result

    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """
        Internal helper to call the LLM client.
        """
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical myth analysis to a file."""
        if self.myth is None:
            raise ValueError("No myth information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        # Create a safe filename from the myth statement
        safe_myth = self.myth.lower()[:50].replace(' ', '_').replace('"', '').replace("'", "")
        base_filename = f"myth_analysis_{safe_myth}"
        
        return save_model_response(result, output_dir / base_filename)
