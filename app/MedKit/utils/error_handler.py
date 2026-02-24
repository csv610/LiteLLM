"""Error handling utilities for MedKit.

This module provides standardized error handling through the ErrorHandler class,
which manages error logging, categorization, and exit code mapping.

Usage:
    from utils.error_handler import ErrorHandler
    from medkit_exceptions import ValidationError, LLMError

    error_handler = ErrorHandler(__name__)

    try:
        process_input(user_input)
    except ValidationError as e:
        exit_code = error_handler.handle_validation_error(e)
    except LLMError as e:
        exit_code = error_handler.handle_llm_error(e)
"""

import logging
import sys
from typing import Optional

from medkit_exceptions import (
    MedKitError,
    ValidationError,
    LLMError,
    FileIOError,
    ConfigurationError,
    MedKitImportError,
)


class ErrorHandler:
    """Centralized error handling with standardized logging and exit codes.

    Provides methods for handling specific error types with appropriate
    logging levels, formatting, and exit code mapping.

    Attributes:
        logger: Logger instance for error messages
        exit_codes: Mapping of error types to exit codes

    Exit Code Convention:
        0: Success
        1: Generic/unknown error
        2: Validation error
        3: LLM error
        4: File I/O error
        5: Configuration error
        6: Import error
    """

    # Exit code convention
    EXIT_CODES = {
        "success": 0,
        "generic": 1,
        "validation": 2,
        "llm": 3,
        "file_io": 4,
        "configuration": 5,
        "import": 6,
    }

    def __init__(self, logger_name: str, verbose: bool = False):
        """Initialize ErrorHandler with logger configuration.

        Args:
            logger_name: Name of the logger (typically __name__)
            verbose: If True, log full exception details (default: False)
        """
        self.logger = logging.getLogger(logger_name)
        self.verbose = verbose

    def handle_validation_error(
        self,
        error: ValidationError,
        exit: bool = False
    ) -> int:
        """Handle validation errors.

        Args:
            error: ValidationError instance
            exit: If True, exit the program with error code

        Returns:
            Exit code (2 for validation errors)
        """
        self.logger.error(f"Validation failed: {error.message}")
        if error.context:
            self.logger.debug(f"  Context: {error.context}")
        if self.verbose and error.original_exception:
            self.logger.debug(
                f"  Original exception: {type(error.original_exception).__name__}: "
                f"{error.original_exception}"
            )

        exit_code = self.EXIT_CODES["validation"]
        if exit:
            sys.exit(exit_code)
        return exit_code

    def handle_llm_error(
        self,
        error: LLMError,
        exit: bool = False
    ) -> int:
        """Handle LLM generation errors.

        Args:
            error: LLMError instance
            exit: If True, exit the program with error code

        Returns:
            Exit code (3 for LLM errors)
        """
        self.logger.error(f"LLM generation failed: {error.message}")
        if error.context:
            self.logger.debug(f"  Context: {error.context}")
        if self.verbose and error.original_exception:
            self.logger.debug(
                f"  Original exception: {type(error.original_exception).__name__}: "
                f"{error.original_exception}"
            )

        exit_code = self.EXIT_CODES["llm"]
        if exit:
            sys.exit(exit_code)
        return exit_code

    def handle_file_io_error(
        self,
        error: FileIOError,
        exit: bool = False
    ) -> int:
        """Handle file I/O errors.

        Args:
            error: FileIOError instance
            exit: If True, exit the program with error code

        Returns:
            Exit code (4 for file I/O errors)
        """
        self.logger.error(f"File I/O operation failed: {error.message}")
        if error.context:
            self.logger.debug(f"  Context: {error.context}")
        if self.verbose and error.original_exception:
            self.logger.debug(
                f"  Original exception: {type(error.original_exception).__name__}: "
                f"{error.original_exception}"
            )

        exit_code = self.EXIT_CODES["file_io"]
        if exit:
            sys.exit(exit_code)
        return exit_code

    def handle_configuration_error(
        self,
        error: ConfigurationError,
        exit: bool = False
    ) -> int:
        """Handle configuration errors.

        Args:
            error: ConfigurationError instance
            exit: If True, exit the program with error code

        Returns:
            Exit code (5 for configuration errors)
        """
        self.logger.error(f"Configuration error: {error.message}")
        if error.context:
            self.logger.debug(f"  Context: {error.context}")
        if self.verbose and error.original_exception:
            self.logger.debug(
                f"  Original exception: {type(error.original_exception).__name__}: "
                f"{error.original_exception}"
            )

        exit_code = self.EXIT_CODES["configuration"]
        if exit:
            sys.exit(exit_code)
        return exit_code

    def handle_import_error(
        self,
        error: MedKitImportError,
        exit: bool = False
    ) -> int:
        """Handle import errors.

        Args:
            error: MedKitImportError instance
            exit: If True, exit the program with error code

        Returns:
            Exit code (6 for import errors)
        """
        self.logger.error(f"Import error: {error.message}")
        if error.context:
            self.logger.debug(f"  Context: {error.context}")
        if self.verbose and error.original_exception:
            self.logger.debug(
                f"  Original exception: {type(error.original_exception).__name__}: "
                f"{error.original_exception}"
            )

        exit_code = self.EXIT_CODES["import"]
        if exit:
            sys.exit(exit_code)
        return exit_code

    def handle_medkit_error(
        self,
        error: MedKitError,
        exit: bool = False
    ) -> int:
        """Handle generic MedKit errors.

        Args:
            error: MedKitError instance
            exit: If True, exit the program with error code

        Returns:
            Exit code (1 for generic errors)
        """
        # Dispatch to specific handlers if applicable
        if isinstance(error, ValidationError):
            return self.handle_validation_error(error, exit=exit)
        elif isinstance(error, LLMError):
            return self.handle_llm_error(error, exit=exit)
        elif isinstance(error, FileIOError):
            return self.handle_file_io_error(error, exit=exit)
        elif isinstance(error, ConfigurationError):
            return self.handle_configuration_error(error, exit=exit)
        elif isinstance(error, MedKitImportError):
            return self.handle_import_error(error, exit=exit)

        # Handle generic MedKitError
        self.logger.error(f"MedKit error: {error.message}")
        if error.context:
            self.logger.debug(f"  Context: {error.context}")
        if self.verbose and error.original_exception:
            self.logger.debug(
                f"  Original exception: {type(error.original_exception).__name__}: "
                f"{error.original_exception}"
            )

        exit_code = self.EXIT_CODES["generic"]
        if exit:
            sys.exit(exit_code)
        return exit_code

    def handle_unexpected_error(
        self,
        error: Exception,
        context: Optional[str] = None,
        exit: bool = False
    ) -> int:
        """Handle unexpected/unclassified errors.

        Args:
            error: Exception instance
            context: Additional context about where/why the error occurred
            exit: If True, exit the program with error code

        Returns:
            Exit code (1 for generic errors)
        """
        self.logger.error(f"Unexpected error: {type(error).__name__}: {error}")
        if context:
            self.logger.debug(f"  Context: {context}")
        if self.verbose:
            self.logger.exception("Full exception traceback:")

        exit_code = self.EXIT_CODES["generic"]
        if exit:
            sys.exit(exit_code)
        return exit_code

    def format_error_message(
        self,
        error: Exception,
        title: str = "Error"
    ) -> str:
        """Format error message for display to user.

        Args:
            error: Exception instance
            title: Title for the error message

        Returns:
            Formatted error message string
        """
        if isinstance(error, MedKitError):
            return f"{title}: {error.message}"
        return f"{title}: {type(error).__name__}: {error}"

    def print_error_message(
        self,
        error: Exception,
        title: str = "Error",
        file=None
    ) -> None:
        """Print formatted error message to stderr.

        Args:
            error: Exception instance
            title: Title for the error message
            file: File to write to (default: stderr)
        """
        if file is None:
            file = sys.stderr

        message = self.format_error_message(error, title)
        print(f"❌ {message}", file=file)


__all__ = ["ErrorHandler"]
