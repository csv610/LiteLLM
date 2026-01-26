"""Base classes and utilities for CLI modules in MedKit.

This module provides:
1. BaseCLI: Base class for CLI entry points with standardized argument parsing
2. BaseGenerator: Base class for generator modules with LLM client handling
3. BasePromptBuilder: Base class for prompt building patterns
4. Utility functions for common CLI operations

All classes are designed to eliminate code duplication across MedKit CLI modules.
"""

import argparse
import logging
import re
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel
from litellm import APIError

# Import centralized logging configuration
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response
from utils.output_formatter import print_result

# Import custom exceptions and error handling
from medkit_exceptions import (
    MedKitError,
    ValidationError,
    LLMError,
    FileIOError,
    ConfigurationError,
)
from utils.error_handler import ErrorHandler


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================


def setup_logging(
    name: str,
    level: int = logging.INFO,
    format_str: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    verbosity: Optional[int] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """Set up logging configuration for a module.

    Args:
        name: Logger name (typically __name__)
        level: Logging level (default: logging.INFO)
        format_str: Log message format string (deprecated, kept for compatibility)
        verbosity: Verbosity level 0-4 (0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG)
        log_file: Optional log file path

    Returns:
        Configured logger instance
    """
    # Determine log file name from module name if not provided
    if log_file is None:
        module_name = name.split('.')[-1] if '.' in name else name
        log_file = f"{module_name}.log"

    # Use centralized logging configuration
    configure_logging(
        log_file=log_file,
        level=level,
        enable_console=True,
        verbosity=verbosity
    )
    return logging.getLogger(name)


def setup_lite_path() -> None:
    """Add the lite package to the Python path.

    This should be called before importing any lite modules.
    Adds the parent directory (4 levels up) to sys.path.
    """
    lite_path = str(Path(__file__).parent.parent.parent.parent)
    if lite_path not in sys.path:
        sys.path.insert(0, lite_path)


def get_logger(name: str, verbose: bool = False) -> logging.Logger:
    """Get a configured logger with appropriate verbosity level.

    Args:
        name: Logger name (typically __name__)
        verbose: If True, set level to DEBUG; otherwise INFO

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    return logger


def ensure_output_dir(output_dir: Path) -> None:
    """Ensure output directory exists.

    Args:
        output_dir: Path to the output directory
    """
    output_dir.mkdir(parents=True, exist_ok=True)


def get_default_output_path(
    output_dir: Path,
    item_name: str,
    suffix: str = "info"
) -> Path:
    """Generate default output file path.

    Args:
        output_dir: Output directory path
        item_name: Name of the item (disease, drug, etc.)
        suffix: File suffix (default: "info")

    Returns:
        Path to the output file
    """
    filename = f"{item_name.lower().replace(' ', '_')}_{suffix}.json"
    return output_dir / filename


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal and invalid characters.

    Args:
        filename: The filename to sanitize

    Returns:
        Sanitized filename
    """
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    sanitized = re.sub(r'\s+', '_', sanitized)
    sanitized = sanitized.strip('. ')
    return sanitized if sanitized else "output"


# ==============================================================================
# BASE CLASSES
# ==============================================================================


class BasePromptBuilder(ABC):
    """Base class for prompt building patterns.

    Provides a standardized interface for creating system and user prompts
    across different CLI modules. Subclasses should implement the abstract methods
    to define domain-specific prompt creation logic.

    Example:
        class DiseasePromptBuilder(BasePromptBuilder):
            @staticmethod
            def create_system_prompt() -> str:
                return "You are a medical expert..."

            @staticmethod
            def create_user_prompt(disease: str) -> str:
                return f"Generate information about {disease}"
    """

    @staticmethod
    @abstractmethod
    def create_system_prompt() -> str:
        """Create the system prompt.

        Returns:
            str: System prompt defining the AI's role and instructions
        """
        pass

    @staticmethod
    @abstractmethod
    def create_user_prompt(*args, **kwargs) -> str:
        """Create the user prompt.

        Returns:
            str: Formatted user prompt for the specific task
        """
        pass


class BaseGenerator(ABC):
    """Base class for generator modules with LLM client handling.

    Provides standardized LLM client initialization, generation flow,
    error handling, and saving functionality. Subclasses should implement
    the abstract methods for domain-specific generation logic.

    Attributes:
        model_config: ModelConfig for LiteClient initialization
        client: LiteClient instance for LLM communication
        logger: Logger for module logging

    Example:
        class DiseaseInfoGenerator(BaseGenerator):
            def generate_text(self, disease: str, structured: bool = False):
                model_input = ModelInput(
                    system_prompt=PromptBuilder.create_system_prompt(),
                    user_prompt=PromptBuilder.create_user_prompt(disease),
                    response_format=DiseaseModel if structured else None,
                )
                return self._ask_llm(model_input)
    """

    def __init__(self, model_config: ModelConfig, logger: Optional[logging.Logger] = None):
        """Initialize the generator with model configuration.

        Args:
            model_config: ModelConfig containing model name, temperature, etc.
            logger: Optional logger instance (uses module logger if not provided)
        """
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.logger = logger or logging.getLogger(__name__)

    @abstractmethod
    def generate_text(self, *args, **kwargs) -> Union[BaseModel, str]:
        """Generate content using the LLM.

        Returns:
            Union[BaseModel, str]: Either a Pydantic model or plain text response
        """
        pass

    def _ask_llm(self, model_input: ModelInput) -> Union[BaseModel, str]:
        """Helper to call LiteClient with standardized error handling.

        Args:
            model_input: ModelInput object with prompts and response format

        Returns:
            Union[BaseModel, str]: LLM response (structured or text)

        Raises:
            LLMError: If LLM generation fails
            ConfigurationError: If model configuration is invalid
        """
        self.logger.debug("Calling LiteClient.generate_text()...")
        try:
            return self.client.generate_text(model_input=model_input)
        except ValueError as e:
            # Configuration issues
            raise ConfigurationError(
                "Invalid model configuration or input format",
                context=f"LiteClient.generate_text() validation failed",
                original_exception=e,
            ) from e
        except (APIError, TimeoutError) as e:
            # LLM API errors and timeouts
            raise LLMError(
                f"LLM API call failed: {type(e).__name__}",
                context=f"Model: {self.model_config.model}, Temperature: {self.model_config.temperature}",
                original_exception=e,
            ) from e
        except Exception as e:
            # Unexpected errors
            raise LLMError(
                f"Unexpected error during LLM generation: {type(e).__name__}",
                context="LiteClient.generate_text()",
                original_exception=e,
            ) from e

    def save(
        self,
        result: Union[BaseModel, str],
        output_path: Path
    ) -> Path:
        """Save the generated result to a file.

        Automatically handles format conversion (JSON to MD for string results)
        and uses lite.utils.save_model_response for consistent saving.

        Args:
            result: The result to save (Pydantic model or string)
            output_path: Path to save the result to

        Returns:
            Path: The actual path where the result was saved
        """
        if isinstance(result, str) and output_path.suffix == ".json":
            output_path = output_path.with_suffix(".md")
        return save_model_response(result, output_path)


class BaseCLI(ABC):
    """Base class for CLI entry points with standardized structure.

    Provides a framework for CLI modules with standardized:
    - Argument parsing
    - Logging configuration
    - Error handling
    - Output formatting
    - Result saving

    Subclasses should implement abstract methods to define domain-specific logic.

    Attributes:
        description: CLI description for help text
        logger: Logger instance for CLI logging
        args: Parsed command-line arguments

    Example:
        class DiseaseInfoCLI(BaseCLI):
            description = "Generate comprehensive disease information"

            def add_arguments(self, parser):
                parser.add_argument("-i", "--disease", required=True)

            def validate_args(self):
                if not self.args.disease.strip():
                    raise ValueError("Disease name cannot be empty")

            def run(self):
                generator = DiseaseInfoGenerator(self.model_config)
                return generator.generate_text(self.args.disease, self.args.structured)
    """

    description: str = "MedKit CLI Tool"
    epilog: str = "Examples:\n  python {module}.py --help"

    def __init__(self, logger_name: str = __name__):
        """Initialize the CLI.

        Args:
            logger_name: Logger name (typically __name__)
        """
        self.logger = logging.getLogger(logger_name)
        self.args = None
        self.model_config = None

    def get_argument_parser(self) -> argparse.ArgumentParser:
        """Create and return the argument parser.

        Subclasses can override to customize parser creation.

        Returns:
            argparse.ArgumentParser: Configured argument parser
        """
        parser = argparse.ArgumentParser(
            description=self.description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=self.epilog,
        )

        # Add common arguments
        self._add_common_arguments(parser)

        # Add domain-specific arguments
        self.add_arguments(parser)

        return parser

    def _add_common_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add common arguments to the parser.

        Args:
            parser: ArgumentParser to add arguments to
        """
        parser.add_argument(
            "-m", "--model",
            default="ollama/gemma3",
            help="LLM model to use (default: ollama/gemma3)"
        )
        parser.add_argument(
            "-t", "--temperature",
            type=float,
            default=0.7,
            help="Temperature for LLM (0-1, default: 0.7)"
        )
        parser.add_argument(
            "-v", "--verbosity",
            type=int,
            default=2,
            choices=[0, 1, 2, 3, 4],
            help="Logging verbosity: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2)"
        )
        parser.add_argument(
            "-o", "--output",
            type=Path,
            help="Output file path for results"
        )
        parser.add_argument(
            "-d", "--output-dir",
            type=Path,
            default=Path("outputs"),
            help="Output directory for results (default: outputs)"
        )
        parser.add_argument(
            "-j", "--json-output",
            action="store_true",
            default=False,
            help="Output results as JSON to stdout"
        )
        parser.add_argument(
            "-s", "--structured",
            action="store_true",
            default=False,
            help="Use structured output (Pydantic model) for the response"
        )

    @abstractmethod
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add domain-specific arguments to the parser.

        Subclasses must implement this to add their specific CLI arguments.

        Args:
            parser: ArgumentParser to add arguments to
        """
        pass

    def validate_args(self) -> None:
        """Validate parsed arguments.

        Subclasses can override to implement domain-specific validation.
        Should raise ValueError for invalid arguments.
        """
        pass

    def _setup_logging(self) -> None:
        """Set up logging based on verbosity argument."""
        configure_logging(
            log_file=f"{self.__class__.__name__.lower()}.log",
            verbosity=self.args.verbosity,
            enable_console=True
        )

    def _get_model_config(self) -> ModelConfig:
        """Get model configuration from arguments.

        Returns:
            ModelConfig: Configured model settings
        """
        return ModelConfig(
            model=self.args.model,
            temperature=self.args.temperature
        )

    def _get_output_path(
        self,
        item_name: str,
        suffix: str = "info"
    ) -> Path:
        """Get output file path.

        Uses explicit --output if provided, otherwise generates default path
        in output directory based on item name and suffix.

        Args:
            item_name: Name of the item (disease, drug, etc.)
            suffix: Output file suffix/type (default: "info")

        Returns:
            Path: Output file path
        """
        if self.args.output:
            return self.args.output

        # Generate default path
        ensure_output_dir(self.args.output_dir)
        filename = f"{sanitize_filename(item_name)}_{suffix}.json"
        return self.args.output_dir / filename

    def _display_result(
        self,
        result: Union[BaseModel, str],
        title: str = "Result"
    ) -> None:
        """Display result using standardized formatting.

        Args:
            result: The result to display
            title: Title for the output panel
        """
        print_result(result, title=title)

    def _output_json(self, result: Union[BaseModel, str]) -> None:
        """Output result as JSON to stdout if requested.

        Args:
            result: The result to output
        """
        if not self.args.json_output:
            return

        if isinstance(result, str):
            print(f"\n{result}")
        else:
            print(f"\n{result.model_dump_json(indent=2)}")

    @abstractmethod
    def run(self) -> Union[BaseModel, str]:
        """Run the main CLI logic.

        Subclasses must implement this to define domain-specific generation logic.

        Returns:
            Union[BaseModel, str]: The generated result
        """
        pass

    def execute(self, args: Optional[List[str]] = None) -> int:
        """Execute the CLI with full error handling.

        This is the main entry point. It orchestrates:
        1. Argument parsing
        2. Validation
        3. Logging setup
        4. Model configuration
        5. Generation
        6. Output/saving
        7. Specific error handling with proper exit codes

        Args:
            args: Command-line arguments (uses sys.argv if not provided)

        Returns:
            int: Exit code (0=success, 2=validation error, 3=LLM error, etc.)
        """
        error_handler = None

        try:
            # Parse arguments
            parser = self.get_argument_parser()
            self.args = parser.parse_args(args)

            # Validate arguments
            try:
                self.validate_args()
            except ValueError as e:
                raise ValidationError(
                    str(e),
                    context=f"{self.__class__.__name__}.validate_args()"
                ) from e

            # Setup logging
            self._setup_logging()
            error_handler = ErrorHandler(__name__, verbose=(self.args.verbosity >= 4))

            # Create model configuration
            try:
                self.model_config = self._get_model_config()
            except Exception as e:
                raise ConfigurationError(
                    "Failed to create model configuration",
                    context=f"Model: {getattr(self.args, 'model', 'unknown')}",
                    original_exception=e,
                ) from e

            self.logger.info("=" * 80)
            self.logger.info(f"Starting {self.__class__.__name__}")
            self.logger.debug(f"Arguments: {self.args}")

            # Run main logic
            try:
                result = self.run()
            except LLMError:
                raise
            except ConfigurationError:
                raise
            except ValidationError:
                raise
            except Exception as e:
                raise LLMError(
                    f"Generation failed: {type(e).__name__}",
                    context=f"{self.__class__.__name__}.run()",
                    original_exception=e,
                ) from e

            if result is None:
                self.logger.error("Failed to generate result")
                return 1

            # Display result
            self._display_result(result)

            # Output JSON if requested
            self._output_json(result)

            # Save result
            self.logger.info("✓ Generation completed successfully")
            self.logger.info("=" * 80)

            return 0

        except ValidationError as e:
            if error_handler:
                error_handler.print_error_message(e, "Validation Error")
                return error_handler.handle_validation_error(e)
            else:
                print(f"\n❌ Validation Error: {e.message}", file=sys.stderr)
                return 2

        except LLMError as e:
            if error_handler:
                error_handler.print_error_message(e, "LLM Error")
                return error_handler.handle_llm_error(e)
            else:
                print(f"\n❌ LLM Error: {e.message}", file=sys.stderr)
                return 3

        except ConfigurationError as e:
            if error_handler:
                error_handler.print_error_message(e, "Configuration Error")
                return error_handler.handle_configuration_error(e)
            else:
                print(f"\n❌ Configuration Error: {e.message}", file=sys.stderr)
                return 5

        except MedKitError as e:
            if error_handler:
                error_handler.print_error_message(e, "MedKit Error")
                return error_handler.handle_medkit_error(e)
            else:
                print(f"\n❌ MedKit Error: {e.message}", file=sys.stderr)
                return 1

        except Exception as e:
            # Fallback for unexpected exceptions
            if error_handler:
                error_handler.print_error_message(e, "Unexpected Error")
                return error_handler.handle_unexpected_error(e, context=f"{self.__class__.__name__}.execute()")
            else:
                print(f"\n❌ Unexpected Error: {type(e).__name__}: {e}", file=sys.stderr)
                self.logger.exception("Full exception details:")
                return 1
