import argparse
import json
import logging
import sys
import os
import re
from pathlib import Path
from typing import Optional, NoReturn
from dataclasses import dataclass

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

from faq_generator_models import FAQ, FAQResponse, VALID_DIFFICULTIES
from faq_generator_prompts import PromptBuilder

# Global logger for the application
logger = logging.getLogger(__name__)


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
        if self.difficulty not in VALID_DIFFICULTIES:
            raise ValueError(
                f"Difficulty must be one of: {', '.join(VALID_DIFFICULTIES)}"
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
        Read content from file with safety checks.

        Args:
            file_path: Path to content file

        Returns:
            File content as string

        Raises:
            ValueError: If file is too large or cannot be read
        """
        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB limit for safety
        
        try:
            path = Path(file_path).resolve()
            if not path.is_file():
                raise ValueError(f"Not a valid file: {file_path}")
            
            if path.stat().st_size > MAX_FILE_SIZE:
                raise ValueError(f"File too large: {path.stat().st_size} bytes (max {MAX_FILE_SIZE})")

            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except (IOError, OSError) as e:
            logger.error(f"IO Error reading {file_path}: {e}")
            raise ValueError(f"Failed to read content file: {e}")

    def generate_text(self, faq_input: FAQInput) -> list[FAQ]:
        """
        Generate FAQs with retry logic and detailed error handling.
        """
        logger.info(f"Starting FAQ generation for: {faq_input.input_source}")
        prompt_builder = PromptBuilder(faq_input.num_faqs, faq_input.difficulty)

        content = None
        if os.path.exists(faq_input.input_source):
            content = self._read_content_file(faq_input.input_source)

        try:
            prompt = prompt_builder.build_content_prompt(content) if content else prompt_builder.build_topic_prompt(faq_input.input_source)
            model_input = ModelInput(user_prompt=prompt, response_format=FAQResponse)

            # Simple retry loop for transient failures
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    logger.debug(f"Generation attempt {attempt + 1}/{max_retries}")
                    response = self.client.generate_text(model_input=model_input)
                    
                    if not isinstance(response, FAQResponse):
                        raise ValueError(f"Invalid response type: {type(response)}")
                    
                    if not response.faqs:
                        raise ValueError("Model returned empty FAQ list")
                    
                    # Semantic sanity check
                    for faq in response.faqs:
                        if len(faq.question) < 10 or len(faq.answer) < 10:
                            raise ValueError("Generated FAQ content too short/low quality")

                    logger.info(f"Successfully generated {len(response.faqs)} FAQs")
                    return response.faqs

                except (RuntimeError, ValueError) as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    continue

        except Exception as e:
            logger.error(f"Critical failure in generate_text: {e}", exc_info=True)
            raise

    def save_to_file(self, faqs: list[FAQ], faq_input: FAQInput) -> str:
        """
        Save FAQs with path sanitization.
        """
        # Sanitize filename
        safe_source = re.sub(r'[^a-zA-Z0-9_-]', '_', Path(faq_input.input_source).name.lower())
        output_filename = f"faq_{safe_source}_{faq_input.difficulty}_{len(faqs)}.json"
        
        # Ensure output_dir is treated safely
        base_dir = Path(faq_input.output_dir).resolve()
        if not base_dir.exists():
            base_dir.mkdir(parents=True, exist_ok=True)
            
        output_path = base_dir / output_filename

        data_to_save = {
            "metadata": {
                "source": faq_input.input_source,
                "difficulty": faq_input.difficulty,
                "count": len(faqs),
                "timestamp": Path(faq_input.output_dir).stat().st_mtime # Placeholder for real timestamp
            },
            "faqs": [faq.model_dump() for faq in faqs]
        }

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4)
            output_path.chmod(0o644)
            logger.info(f"Results archived to {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Archive failure: {e}")
            raise IOError(f"Could not save results: {e}")
