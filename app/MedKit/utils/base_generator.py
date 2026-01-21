"""Base generator class for all MedKit CLI modules.

This module provides the base generator class that all CLI modules
should inherit from to reduce code duplication and ensure consistent patterns.
"""

import json
import logging
from pathlib import Path
from typing import Optional, TypeVar, Generic
from pydantic import BaseModel

# Setup lite path before importing
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging

from .base_config import BaseConfig

# Generic type for the output model
T = TypeVar('T', bound=BaseModel)


class BaseGenerator(Generic[T]):
    """Base class for all MedKit generators.

    This class provides common functionality for all generators including:
    - LiteClient initialization
    - Save functionality

    Attributes:
        client: LiteClient instance
        logger: Logger instance
    """

    def __init__(
        self,
        model_config: ModelConfig,
        logger_name: Optional[str] = None
    ):
        """Initialize the generator.

        Args:
            model_config: ModelConfig object with model settings
            logger_name: Optional logger name (defaults to class name)
        """
        self.client = LiteClient(model_config)

        # Setup logger
        if logger_name is None:
            logger_name = self.__class__.__name__

        self.logger = logging.getLogger(logger_name)
        self.logger.info(f"Initialized {self.__class__.__name__}")

    def generate_with_prompt(
        self,
        prompt: str,
        response_format: type[T],
        system_prompt: Optional[str] = None
    ) -> T:
        """Generate output using LiteClient with a prompt.

        Args:
            prompt: User prompt for generation
            response_format: Pydantic model class for response format
            system_prompt: Optional system prompt

        Returns:
            Generated output as Pydantic model instance

        Raises:
            Exception: If generation fails
        """
        self.logger.info("Calling LiteClient.generate_text()...")
        self.logger.debug(f"Prompt: {prompt}")

        try:
            model_input = ModelInput(
                user_prompt=prompt,
                response_format=response_format,
            )
            if system_prompt:
                model_input.system_prompt = system_prompt

            result = self.client.generate_text(model_input=model_input)
            self.logger.info("✓ Successfully generated output")
            return result

        except Exception as e:
            self.logger.error(f"✗ Error generating output: {e}")
            self.logger.exception("Full exception details:")
            raise

    def save(self, data: BaseModel, output_path: Path) -> None:
        """Save data to a JSON file.

        Args:
            data: Pydantic model instance to save
            output_path: Path where the JSON file should be saved
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Saving output to: {output_file}")

        try:
            with open(output_file, "w") as f:
                json.dump(data.model_dump(), f, indent=2)
            file_size = output_file.stat().st_size
            self.logger.info(f"✓ Successfully saved output")
            self.logger.info(f"File: {output_file}")
            self.logger.info(f"File size: {file_size} bytes")
        except Exception as e:
            self.logger.error(f"✗ Error saving output: {e}")
            self.logger.exception("Full exception details:")
            raise

    def get_output_path(
        self,
        item_name: str,
        suffix: str = "info",
        custom_path: Optional[Path] = None,
        output_dir: Path = Path("outputs")
    ) -> Path:
        """Determine output path for generated data.

        Args:
            item_name: Name of the item (disease, drug, etc.)
            suffix: File suffix (default: "info")
            custom_path: Optional custom output path
            output_dir: Output directory (default: "outputs")

        Returns:
            Path to the output file
        """
        if custom_path:
            return custom_path

        filename = f"{item_name.lower().replace(' ', '_')}_{suffix}.json"
        return output_dir / filename
