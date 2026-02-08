#!/usr/bin/env python3
"""
Medical Procedure Output Evaluation module.

This module provides the MedicalProcedureEvaluator class for critically reviewing
generated medical procedure information against high medical standards.
"""

import logging
import re
import json
from pathlib import Path
from typing import Optional, Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from eval_medical_procedure_models import MedicalProcedureEvaluationModel, ModelOutput
from eval_medical_procedure_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalProcedureEvaluator:
    """Evaluate medical procedure information using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the evaluator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.procedure_name: Optional[str] = None
        logger.debug(f"Initialized MedicalProcedureEvaluator")

    def generate_text(self, file_path: Union[str, Path], structured: bool = True) -> ModelOutput:
        """Read content from a file and evaluate it."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise

        # Infer procedure name from filename
        procedure_name = file_path.stem.replace('_', ' ').title()
        self.procedure_name = procedure_name
        logger.info(f"Inferred procedure name from filename: {procedure_name}")

        if not content or not content.strip():
            raise ValueError("Content to evaluate cannot be empty")

        logger.debug(f"Starting evaluation for procedure: {procedure_name}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(procedure_name, content)
        
        response_format = None
        if structured:
            response_format = MedicalProcedureEvaluationModel

        logger.debug(f"System Prompt: {system_prompt}")
        
        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text() for evaluation...")
        try:
            result = self.client.generate_text(model_input=model_input)
            
            if structured:
                logger.debug("✓ Successfully generated structured evaluation")
                return ModelOutput(data=result.data, markdown=result.markdown)

            logger.debug("✓ Successfully evaluated medical procedure information (unstructured)")
            return ModelOutput(markdown=result.markdown)
        except Exception as e:
            logger.error(f"✗ Error evaluating medical procedure information: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the evaluation report to a file."""
        if self.procedure_name is None:
            raise ValueError("No procedure evaluated. Call evaluate_text or evaluate_file first.")
        
        base_filename = f"{self.procedure_name.lower().replace(' ', '_')}_eval"
        
        return save_model_response(result, output_dir / base_filename)
