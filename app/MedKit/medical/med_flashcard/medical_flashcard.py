#!/usr/bin/env python3
"""
Medical Label Explainer module.

This module provides the core MedicalLabelExplainer class for extracting
and explaining medical labels from images.
"""

import logging
from pathlib import Path
from typing import Union, List, Tuple

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from medical_flashcard_models import MedicalLabelInfoModel, ModelOutput
from medical_flashcard_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalLabelExtractor:
    """Extracts medical terms from an image."""

    def __init__(self, config: ModelConfig):
        self.client = LiteClient(config)

    def extract_terms(self, image_path: str) -> List[str]:
        """Extracts medical terms from an image."""
        logger.debug(f"Extracting terms from image: {image_path}")
       
        prompt = PromptBuilder.create_text_extraction_prompt()
        model_input = ModelInput(
            user_prompt=prompt,
            image_path=image_path
        )
        
        try:
            response = self.client.generate_text(model_input=model_input)
            text = ""
            if isinstance(response, str):
                text = response
            elif hasattr(response, 'markdown') and response.markdown:
                text = response.markdown
            
            if text:
                # Split by comma or newline and clean up
                import re
                terms = [t.strip() for t in re.split(r'[,\n]', text) if t.strip()]
                return terms
            return []
        except Exception as e:
            logger.error(f"Error extracting terms from image: {e}")
            raise


class MedicalTermExplainer:
    """Generates comprehensive medical information for medical terms."""

    def __init__(self, config: ModelConfig):
        self.client = LiteClient(config)

    def generate_text(self, labels: List[str], structured: bool = False) -> List[Tuple[str, ModelOutput]]:
        """Generates comprehensive medical information for a list of terms."""
        results = []
        for label in labels:
            print(f"Explaining: {label}")
            output = self.explain_label(label, structured)
            results.append((label, output))
        return results

    def explain_label(self, label: str, structured: bool = False) -> ModelOutput:
        """Generates comprehensive medical information for a term."""
        if not term or not str(term).strip():
            raise ValueError("Term name cannot be empty for report generation.")

        logger.debug(f"Starting medical information generation for: {term}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(label)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
           response_format = MedicalLabelInfoModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.client.generate_text(model_input=model_input)
            logger.debug("✓ Successfully generated medical information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating medical information: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path, term: str) -> Path:
        """Saves the medical information to a file."""
        if not term:
            raise ValueError("Term name must be provided to save.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{term.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)
