#!/usr/bin/env python3
"""
Medical Facts Checker Analysis module.

This module provides the core MedicalFactsChecker class for analyzing
medical statements for factual accuracy.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from medical_facts_checker_models import MedicalFactFictionAnalysisModel, ModelOutput
from medical_facts_checker_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalFactsChecker:
    """Analyzes medical statements for factual accuracy."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the facts checker."""
        self.client = LiteClient(model_config=model_config)
        self.statement: Optional[str] = None
        self.output_path: Optional[Path] = None
        logger.debug(f"Initialized MedicalFactsChecker")

    def generate_text(self, statement: str, structured: bool = False) -> ModelOutput:
        """
        Analyze a statement and determine if it is a fact or fiction.

        Args:
            statement: The statement to analyze.
            structured: Whether to use structured output

        Returns:
            The generated FactFictionAnalysis object.
        
        Raises:
            ValueError: If statement is empty.
        """
        if not statement or not statement.strip():
            raise ValueError("Statement cannot be empty")

        # Store the statement for later use in save
        self.statement = statement
        logger.debug(f"Starting medical facts analysis for: {statement}")

        response_format = None
        if structured:
            response_format = MedicalFactFictionAnalysisModel

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(statement)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self._ask_llm(model_input)
            logger.debug("✓ Successfully analyzed medical statement")
            return result
        except Exception as e:
            logger.error(f"✗ Error analyzing medical statement: {e}")
            raise

    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """
        Internal helper to call the LLM client.
        """
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical facts analysis to a file."""
        if self.statement is None:
            raise ValueError("No statement information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.statement.lower().replace(' ', '_')}_facts_analysis"
        
        return save_model_response(result, output_dir / base_filename)
