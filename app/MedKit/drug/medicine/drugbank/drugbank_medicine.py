#!/usr/bin/env python3
"""
DrugBank Medicine Information module.

This module provides the core DrugBankMedicine class for fetching
comprehensive medicine information using LiteClient.
"""

import logging
import re
from pathlib import Path
from typing import Optional, Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from drugbank_medicine_models import MedicineInfo

logger = logging.getLogger(__name__)


class DrugBankMedicine:
    """Fetches comprehensive medicine information using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the DrugBank medicine fetcher."""
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.medicine_name = None  # Store the medicine name for later use in save
        logger.debug(f"Initialized DrugBankMedicine using model: {model_config.model}")

    def generate_text(self, medicine_name: str, structured: bool = False) -> Union[MedicineInfo, str]:
        """Fetch comprehensive medicine information (pharmacology, safety, etc.)."""
        if not medicine_name or not medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")

        # Store the medicine name for later use in save
        self.medicine_name = medicine_name
        logger.debug(f"Starting medicine information fetch for: {medicine_name}")

        user_prompt = f"Provide detailed information about the medicine {medicine_name}."
        model_input = ModelInput(
            user_prompt=user_prompt,
            response_format=MedicineInfo if structured else None,
        )
        
        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self._ask_llm(model_input)
            logger.debug(f"✓ Successfully fetched info for {medicine_name}")
            return result
        except Exception as e:
            logger.error(f"✗ Error during medicine info fetch: {e}")
            raise

    def _ask_llm(self, model_input: ModelInput) -> Union[MedicineInfo, str]:
        """Helper to call LiteClient with error handling."""
        logger.debug(f"Sending request to LLM client for model: {self.model_config.model}")
        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"✗ Error during medicine info fetch: {e}")
            logger.exception("Full exception details:")
            raise

    def save(self, result: Union[MedicineInfo, str], output_dir: Path) -> Path:
        """Save the medicine information to a file."""
        if self.medicine_name is None:
            raise ValueError("No medicine name information available. Call generate_text first.")
        
        # Generate sanitized filename
        sanitized_name = self._sanitize_filename(self.medicine_name)
        base_filename = f"{sanitized_name}_medicine_info"
        
        return save_model_response(result, output_dir / base_filename)

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal and invalid characters."""
        sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
        sanitized = re.sub(r'\s+', '_', sanitized)
        sanitized = sanitized.strip('. ')
        return sanitized if sanitized else "medicine"
