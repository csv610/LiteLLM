#!/usr/bin/env python3
"""
Symptom-to-Drug Analysis module.

This module provides the core SymptomDrugs class for listing medications
prescribed for specific symptoms based on clinical guidance.
"""

import logging
from pathlib import Path
from typing import Optional, Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from symptom_drugs_models import SymptomDrugAnalysisModel, ModelOutput
from symptom_drugs_prompts import PromptBuilder, SymptomInput, PromptStyle

logger = logging.getLogger(__name__)


class SymptomDrugs:
    """Analyzes symptoms to list medications typically used for treatment."""
    
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.config = None  # Store the configuration for later use in save
        logger.debug(f"Initialized SymptomDrugs")

    def generate_text(self, config: SymptomInput, structured: bool = False) -> ModelOutput:
        """
        Analyzes symptoms and lists potential medications for treatment.

        Args:
            config: Configuration and input for analysis
            structured: Whether to use structured output

        Returns:
            ModelOutput: The analysis result
        """
        # Store the configuration for later use in save
        self.config = config
        logger.debug(f"Starting symptom-to-drug analysis")
        logger.debug(f"Symptom: {config.symptom_name}")

        user_prompt = PromptBuilder.create_user_prompt(config)
        response_format = None
        if structured:
            response_format = SymptomDrugAnalysisModel

        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=user_prompt,
            response_format=response_format,
        )
        result = self._ask_llm(model_input)
        
        logger.debug(f"✓ Successfully analyzed symptom: {config.symptom_name}")
        return result

    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Helper to call LiteClient with error handling."""
        logger.debug("Calling LiteClient...")
        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"✗ Error during LLM analysis: {e}")
            logger.exception("Full exception details:")
            raise
            
    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the symptom-to-drug analysis to a file."""
        if self.config is None:
            raise ValueError("No configuration information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        symptom_safe = self.config.symptom_name.lower().replace(' ', '_')
        base_filename = f"{symptom_safe}_drug_recommendations"
        
        return save_model_response(result, output_dir / base_filename)
