"""
Drug Identifier module.

This module provides the DrugIdentifier class for determining if a drug
is well-known in the industry.
"""

import logging
from pathlib import Path
from typing import Optional

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from .drug_recognizer_model import DrugIdentifierModel, ModelOutput
from .drug_recognizer_prompts import PromptBuilder, DrugIdentifierInput

logger = logging.getLogger(__name__)


class DrugIdentifier:
    """Identifies drugs and their industry recognition status."""
    
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.config = None
        logger.debug(f"Initialized DrugIdentifier")

    def identify_drug(self, drug_name: str, structured: bool = True) -> ModelOutput:
        """
        Identifies if a drug is well-known in the industry.

        Args:
            drug_name: Name of the drug to identify
            structured: Whether to use structured output

        Returns:
            ModelOutput: The identification result
        """
        config = DrugIdentifierInput(drug_name=drug_name)
        self.config = config
        
        logger.debug(f"Starting drug identification for: {drug_name}")

        user_prompt = PromptBuilder.create_user_prompt(config)
        response_format = None
        if structured:
            response_format = DrugIdentifierModel

        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=user_prompt,
            response_format=response_format,
        )
        
        result = self._ask_llm(model_input)
        
        logger.debug(f"✓ Successfully identified drug: {drug_name}")
        return result

    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Helper to call LiteClient with error handling."""
        logger.debug("Calling LiteClient...")
        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"✗ Error during LLM analysis: {e}")
            raise
            
    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the drug identification analysis to a file."""
        if self.config is None:
            raise ValueError("No configuration information available. Call identify_drug first.")
        
        drug_safe = self.config.drug_name.lower().replace(' ', '_')
        base_filename = f"{drug_safe}_identification"
        
        return save_model_response(result, output_dir / base_filename)
