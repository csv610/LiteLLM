import argparse
import json
import sys
import os
import re
from pathlib import Path
from typing import Optional, NoReturn
from dataclasses import dataclass

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

from faq_generator_models import FAQ, FAQResponse
from faq_generator_prompts import PromptBuilder

# ==============================================================================
# Configuration Dataclass
# ==============================================================================

@dataclass
class FAQInput:
    """Input parameters for FAQ generation."""
    input_source: str  # Can be a topic or a filename
    num_faqs: int
    difficulty: str
    output_dir: str = "."

    VALID_DIFFICULTIES = ["simple", "medium", "hard", "research"]

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        self._validate()

    def _validate(self) -> None:
        """
        Validate configuration parameters.

        Raises:
            ValueError: If any parameter is invalid
        """
        # Validate input_source
        if not self.input_source or len(self.input_source) < 1:
            raise ValueError("Input source (topic or filename) must be provided")

        # Validate num_faqs
        if self.num_faqs < 1 or self.num_faqs > 100:
            raise ValueError(
                f"Number of FAQs must be between 1 and 100, got {self.num_faqs}"
            )

        # Validate difficulty
        if self.difficulty not in self.VALID_DIFFICULTIES:
            raise ValueError(
                f"Difficulty must be one of: {', '.join(self.VALID_DIFFICULTIES)}"
            )

        # Validate output directory
        if not os.path.isdir(self.output_dir):
            raise ValueError(f"Output directory not found: {self.output_dir}")

    def is_file(self) -> bool:
        """
        Check if input_source is a file or a topic.

        Returns:
            True if input_source is a file path, False if it's a topic
        """
        return os.path.exists(self.input_source)

    def get_topic(self) -> Optional[str]:
        """
        Get topic if input_source is a topic string.

        Returns:
            Topic string or None if input_source is a file
        """
        if not self.is_file():
            return self.input_source
        return None

    def get_file_path(self) -> Optional[str]:
        """
        Get file path if input_source is a file.

        Returns:
            File path or None if input_source is a topic
        """
        if self.is_file():
            return self.input_source
        return None


# ==============================================================================
# FAQ Generator Class
# ==============================================================================

class FAQGenerator:
    """Generate frequently asked questions on a given topic with selectable difficulty levels."""

    def __init__(self, config: ModelConfig):
        """
        Initialize FAQ generator.

        Args:
            config: ModelConfig with model settings
        """
        self.model_config = config
        self.model = config.model or "ollama/gemma3"
        self.client = LiteClient(model_config=self.model_config)

    def _read_content_file(self, file_path: str) -> str:
        """
        Read content from file.

        Args:
            file_path: Path to content file

        Returns:
            File content as string

        Raises:
            ValueError: If file cannot be read
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except IOError as e:
            raise ValueError(f"Failed to read content file: {e}")

    def generate_text(self, faq_input: FAQInput) -> list[FAQ]:
        """
        Generate FAQs based on input parameters.

        Args:
            faq_input: FAQInput object containing generation parameters

        Returns:
            List of FAQ instances

        Raises:
            ValueError: If parameters are invalid
            RuntimeError: If API call fails or required credentials are missing
        """
        # Initialize prompt builder with parameters
        prompt_builder = PromptBuilder(faq_input.num_faqs, faq_input.difficulty)

        # Read content file if input_source is a file
        content = None
        if os.path.exists(faq_input.input_source):
            content = self._read_content_file(faq_input.input_source)

        try:
            # Create prompt based on content or topic
            if content:
                prompt = prompt_builder.build_content_prompt(content)
            else:
                prompt = prompt_builder.build_topic_prompt(faq_input.input_source)

            # Create ModelInput with prompt and response format
            model_input = ModelInput(
                user_prompt=prompt,
                response_format=FAQResponse
            )

            # Generate text using LiteClient (returns parsed FAQResponse)
            response = self.client.generate_text(model_input=model_input)

            if not isinstance(response, FAQResponse):
                raise ValueError("Expected FAQResponse object from model")

            if not response.faqs:
                raise ValueError("No FAQs returned in response")

            return response.faqs

        except Exception as e:
            # Re-raise exceptions to be handled by LiteClient
            raise

    def save_to_file(self, faqs: list[FAQ], faq_input: FAQInput) -> str:
        """
        Save FAQs to a JSON file.

        Args:
            faqs: List of FAQ objects to save
            faq_input: FAQInput object containing generation parameters

        Returns:
            Path to saved file

        Raises:
            IOError: If file cannot be written
        """
        # Generate automatic filename
        safe_source = re.sub(r'[^a-zA-Z0-9_-]', '_', faq_input.input_source.lower())
        # Remove file extension if present
        safe_source = re.sub(r'\.[^.]+$', '', safe_source)
        output_filename = f"faq_{safe_source}_{faq_input.difficulty}_{len(faqs)}.json"
        output_path = os.path.join(faq_input.output_dir, output_filename)

        source_label = "file" if os.path.exists(faq_input.input_source) else "topic"
        data_to_save = {
            "source_type": source_label,
            "source": faq_input.input_source,
            "difficulty": faq_input.difficulty,
            "faqs": [faq.model_dump() for faq in faqs]
        }

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4)

            os.chmod(output_path, 0o644)
            return output_path

        except IOError as e:
            raise
