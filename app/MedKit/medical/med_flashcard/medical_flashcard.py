#!/usr/bin/env python3
"""
Medical Flashcard module.

This module provides the core MedicalFlashcardGenerator class for generating
comprehensive medical flashcard information based on provided configuration.
"""

import logging
from pathlib import Path
from typing import Union, List, Tuple

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from medical_flashcard_models import MedicalFlashcardInfoModel, ModelOutput
from medical_flashcard_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalFlashcardGenerator:
    """Generates comprehensive medical flashcard information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.term = None  # Store the term being analyzed
        logger.debug(f"Initialized MedicalFlashcardGenerator")

    def extract_terms(self, image_path: str) -> List[str]:
        """Extracts medical terms from an image."""
        logger.debug(f"Extracting terms from image: {image_path}")
        
        prompt = PromptBuilder.create_image_analysis_prompt()
        model_input = ModelInput(
            user_prompt=prompt,
            image_path=image_path
        )
        
        try:
            response = self.ask_llm(model_input)
            text = ""
            if isinstance(response, str):
                text = response
            elif hasattr(response, 'markdown') and response.markdown:
                text = response.markdown
            
            if text:
                # Split by comma and clean up
                terms = [t.strip() for t in text.split(",") if t.strip()]
                return terms
            return []
        except Exception as e:
            logger.error(f"Error extracting terms from image: {e}")
            raise

    def explain_term(self, term: str, structured: bool = False) -> ModelOutput:
        """Generates comprehensive medical flashcard information for a term."""
        if not term or not str(term).strip():
            raise ValueError("Term name cannot be empty for report generation.")

        # Store the term for later use in save
        self.term = term
        logger.debug(f"Starting medical flashcard information generation for: {term}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(term)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
           response_format = MedicalFlashcardInfoModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated flashcard information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating flashcard information: {e}")
            raise

    def generate_text(self, image_path: str, structured: bool = False) -> List[Tuple[str, ModelOutput]]:
        """
        Orchestrates the extraction and explanation of medical terms from an image.
        """
        terms = self.extract_terms(image_path)
        for term in terms:
            print(term)
        logger.info(f"Identified terms: {terms}")
        
        results = []
        for term in terms:
            print(term)
            output = self.explain_term(term, structured)
            results.append((term, output))
        return results

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path, term: str = None) -> Path:
        """Saves the flashcard information to a file."""
        term_to_use = term or self.term
        if term_to_use is None:
            raise ValueError("No flashcard information available. Call generate_text first or provide a term.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{term_to_use.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)
