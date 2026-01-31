#!/usr/bin/env python3
"""
Drugs Comparison module.

This module provides the core DrugsComparison class for comparing two medicines
across clinical, regulatory, and practical metrics.
"""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from drugs_comparison_models import MedicinesComparisonResult
from drugs_comparison_prompts import PromptBuilder

logger = logging.getLogger(__name__)


@dataclass
class DrugsComparisonInput:
    """Configuration and input for medicines comparison."""
    medicine1: str
    medicine2: str
    use_case: Optional[str] = None
    patient_age: Optional[int] = None
    patient_conditions: Optional[str] = None
    prompt_style: str = "detailed"


class DrugsComparison:
    """Compares two medicines based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)
        self.config = None  # Store the configuration for later use in save
        logger.debug(f"Initialized DrugsComparison")

    def generate_text(self, config: DrugsComparisonInput, structured: bool = False) -> Union[MedicinesComparisonResult, str]:
        """Compares two medicines across clinical, regulatory, and practical metrics."""
        # Store the configuration for later use in save
        self.config = config
        self._validate_input(config)

        logger.debug(f"Starting medicines comparison analysis")
        logger.debug(f"Medicine 1: {config.medicine1}")
        logger.debug(f"Medicine 2: {config.medicine2}")

        context = self._prepare_context(config)
        logger.debug(f"Context: {context}")

        user_prompt = PromptBuilder.create_user_prompt(config.medicine1, config.medicine2, context)
        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=user_prompt,
            response_format=MedicinesComparisonResult if structured else None,
        )
        result = self._ask_llm(model_input)

        logger.debug(f"✓ Successfully compared medicines")
        return result

    def _validate_input(self, config: DrugsComparisonInput) -> None:
        """Validate input parameters."""
        if not config.medicine1 or not config.medicine1.strip():
            raise ValueError("Medicine 1 name cannot be empty")
        if not config.medicine2 or not config.medicine2.strip():
            raise ValueError("Medicine 2 name cannot be empty")
        if config.patient_age is not None and (config.patient_age < 0 or config.patient_age > 150):
            raise ValueError("Age must be between 0 and 150 years")

    def _prepare_context(self, config: DrugsComparisonInput) -> str:
        """Build the analysis context string from input parameters."""
        context_parts = [f"Comparing {config.medicine1} and {config.medicine2}"]
        if config.use_case:
            context_parts.append(f"Use case: {config.use_case}")
            logger.debug(f"Use case: {config.use_case}")
        if config.patient_age is not None:
            context_parts.append(f"Patient age: {config.patient_age} years")
            logger.debug(f"Patient age: {config.patient_age}")
        if config.patient_conditions:
            context_parts.append(f"Patient conditions: {config.patient_conditions}")
            logger.debug(f"Patient conditions: {config.patient_conditions}")
        return ". ".join(context_parts) + "."

    def _ask_llm(self, model_input: ModelInput) -> Union[MedicinesComparisonResult, str]:
        """Helper to call LiteClient with error handling."""
        logger.debug("Calling LiteClient.generate_text()...")
        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"✗ Error during LLM analysis: {e}")
            logger.exception("Full exception details:")
            raise

    def save(self, result: Union[MedicinesComparisonResult, str], output_dir: Path) -> Path:
        """Saves the drugs comparison analysis to a file."""
        if self.config is None:
            raise ValueError("No configuration information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        medicine1_safe = self.config.medicine1.lower().replace(' ', '_')
        medicine2_safe = self.config.medicine2.lower().replace(' ', '_')
        base_filename = f"{medicine1_safe}_vs_{medicine2_safe}_comparison"
        
        return save_model_response(result, output_dir / base_filename)
