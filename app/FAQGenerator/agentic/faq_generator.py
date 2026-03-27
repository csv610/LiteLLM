import json
import logging
import os
import re
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

from faq_generator_models import FAQ, FAQResponse, ReviewedFAQResponse, VALID_DIFFICULTIES
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
        # Clean input strings
        if isinstance(self.input_source, str):
            self.input_source = self.input_source.strip()
        if isinstance(self.difficulty, str):
            self.difficulty = self.difficulty.lower().strip()
            
        self._validate()

    def _validate(self) -> None:
        """
        Validate configuration parameters.

        Raises:
            ValueError: If any parameter is invalid
        """
        # Validate input_source
        if not self.input_source:
            raise ValueError("Input source (topic or filename) cannot be empty")

        if not os.path.exists(self.input_source):
            if len(self.input_source) < 2 or len(self.input_source) > 100:
                raise ValueError("Topic must be 2-100 characters (or provide valid file path)")

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
    """Generate FAQs with a generator agent followed by a reviewer agent."""

    def __init__(self, config: Optional[ModelConfig] = None, *, model_config: Optional[ModelConfig] = None):
        """
        Initialize FAQ generator.

        Args:
            config: ModelConfig with model settings
            model_config: Backward-compatible keyword alias for config
        """
        resolved_config = model_config or config
        if resolved_config is None:
            raise ValueError("A ModelConfig instance is required")

        self.model_config = resolved_config
        self.model = resolved_config.model or "ollama/gemma3"
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

    def _validate_faqs(self, faqs: list[FAQ]) -> None:
        """Run lightweight structural checks on generated FAQs."""
        if not faqs:
            raise ValueError("Model returned empty FAQ list")

        seen_questions = set()
        for faq in faqs:
            normalized_question = faq.question.strip().lower()
            if normalized_question in seen_questions:
                raise ValueError("Generated FAQ list contains duplicate questions")
            seen_questions.add(normalized_question)

            if len(faq.question) < 10 or len(faq.answer) < 10:
                raise ValueError("Generated FAQ content too short/low quality")

    def _run_stage(self, *, prompt: str, response_format: type[FAQResponse], stage_name: str) -> FAQResponse:
        """
        Execute one agent stage with retries.

        Args:
            prompt: User prompt for the stage
            response_format: Expected structured response model
            stage_name: Name used for logs and errors

        Returns:
            Parsed response object
        """
        model_input = ModelInput(user_prompt=prompt, response_format=response_format)
        max_retries = 3

        for attempt in range(max_retries):
            try:
                logger.debug(f"{stage_name} attempt {attempt + 1}/{max_retries}")
                response = self.client.generate_text(model_input=model_input)

                if not isinstance(response, response_format):
                    raise ValueError(f"{stage_name} returned invalid response type: {type(response)}")

                self._validate_faqs(response.faqs)
                return response
            except (RuntimeError, ValueError) as e:
                if attempt == max_retries - 1:
                    raise
                logger.warning(f"{stage_name} attempt {attempt + 1} failed: {e}. Retrying...")

        raise RuntimeError(f"{stage_name} failed unexpectedly")

    def generate_text(self, faq_input: FAQInput) -> list[FAQ]:
        """
        Generate FAQs with a generator stage and a reviewer stage.
        """
        logger.info(f"Starting FAQ generation for: {faq_input.input_source}")
        prompt_builder = PromptBuilder(faq_input.num_faqs, faq_input.difficulty)

        content = None
        if os.path.exists(faq_input.input_source):
            content = self._read_content_file(faq_input.input_source)

        try:
            generation_prompt = (
                prompt_builder.build_content_prompt(content)
                if content else
                prompt_builder.build_topic_prompt(faq_input.input_source)
            )
            generated_response = self._run_stage(
                prompt=generation_prompt,
                response_format=FAQResponse,
                stage_name="Generator agent"
            )

            review_prompt = prompt_builder.build_review_prompt(
                source=faq_input.input_source,
                faqs=generated_response.faqs,
                content=content
            )
            reviewed_response = self._run_stage(
                prompt=review_prompt,
                response_format=ReviewedFAQResponse,
                stage_name="Reviewer agent"
            )

            logger.info(f"Successfully generated and reviewed {len(reviewed_response.faqs)} FAQs")
            return reviewed_response.faqs

        except Exception as e:
            logger.error(f"Critical failure in generate_text: {e}", exc_info=True)
            raise


# ==============================================================================
# Persistence Class
# ==============================================================================

class DataExporter:
    """Handles the persistence of generated FAQs to the filesystem."""

    @staticmethod
    def export_to_json(faqs: list[FAQ], faq_input: FAQInput) -> str:
        """
        Save FAQs to a JSON file with path sanitization.

        Args:
            faqs: List of generated FAQ objects
            faq_input: Input configuration used for generation

        Returns:
            Path to the saved file as a string
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
