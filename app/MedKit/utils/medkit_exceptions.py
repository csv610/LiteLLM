"""Custom exception classes for MedKit.

This module provides a hierarchy of custom exceptions for consistent error handling
across the MedKit codebase. All exceptions inherit from MedKitError base class.

Exception Hierarchy:
    MedKitError
    ├── ValidationError
    ├── LLMError
    ├── FileIOError
    ├── ConfigurationError
    └── ImportError

Usage:
    from medkit_exceptions import ValidationError, LLMError

    try:
        process_input(user_input)
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
    except LLMError as e:
        logger.error(f"LLM generation failed: {e}")
"""

from typing import Optional


class MedKitError(Exception):
    """Base exception class for all MedKit errors.

    This is the root exception for the MedKit error hierarchy. All custom
    exceptions in MedKit inherit from this class, allowing for broad error
    catching when needed while still supporting specific error handling.

    Attributes:
        message: Human-readable error message
        context: Additional context information
        original_exception: The original exception that caused this error (if applicable)
    """

    def __init__(
        self,
        message: str,
        context: Optional[str] = None,
        original_exception: Optional[Exception] = None
    ):
        """Initialize MedKitError with message, context, and original exception.

        Args:
            message: Human-readable error message
            context: Additional context about the error (e.g., function name, input values)
            original_exception: The original exception that caused this error
        """
        self.message = message
        self.context = context
        self.original_exception = original_exception
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """Format the complete error message with context.

        Returns:
            Formatted error message including context if available
        """
        message = f"[MedKitError] {self.message}"
        if self.context:
            message += f"\nContext: {self.context}"
        if self.original_exception:
            message += f"\nCaused by: {type(self.original_exception).__name__}: {self.original_exception}"
        return message

    def __str__(self) -> str:
        """Return formatted error message.

        Returns:
            Formatted error message
        """
        return self._format_message()

    def __repr__(self) -> str:
        """Return representation of the exception.

        Returns:
            String representation including class name and message
        """
        return f"{self.__class__.__name__}({self.message!r})"


class ValidationError(MedKitError):
    """Exception raised for input validation failures.

    Raised when user input, configuration, or arguments fail validation checks.
    This includes type mismatches, empty values, invalid formats, etc.

    Example:
        if not disease_name or not disease_name.strip():
            raise ValidationError(
                "Disease name cannot be empty",
                context="disease_info_cli.run()"
            )
    """

    def _format_message(self) -> str:
        """Format validation error message.

        Returns:
            Formatted error message with validation prefix
        """
        message = f"[ValidationError] {self.message}"
        if self.context:
            message += f"\nContext: {self.context}"
        if self.original_exception:
            message += f"\nCaused by: {type(self.original_exception).__name__}: {self.original_exception}"
        return message


class LLMError(MedKitError):
    """Exception raised for LLM generation failures.

    Raised when the LLM client fails to generate text, API errors occur,
    or response parsing fails. This can include timeouts, authentication
    errors, invalid responses, etc.

    Example:
        try:
            response = client.generate_text(model_input)
        except APIError as e:
            raise LLMError(
                "Failed to generate response from LLM",
                context=f"Model: {model_name}, Temperature: {temp}",
                original_exception=e
            )
    """

    def _format_message(self) -> str:
        """Format LLM error message.

        Returns:
            Formatted error message with LLM prefix and details
        """
        message = f"[LLMError] {self.message}"
        if self.context:
            message += f"\nContext: {self.context}"
        if self.original_exception:
            message += f"\nCaused by: {type(self.original_exception).__name__}: {self.original_exception}"
        return message


class FileIOError(MedKitError):
    """Exception raised for file read/write failures.

    Raised when file operations fail, including missing files, permission
    errors, corrupt data, etc.

    Example:
        try:
            with open(output_path, 'w') as f:
                json.dump(data, f)
        except (IOError, OSError) as e:
            raise FileIOError(
                f"Failed to write output to {output_path}",
                context="save_result()",
                original_exception=e
            )
    """

    def _format_message(self) -> str:
        """Format file IO error message.

        Returns:
            Formatted error message with FileIO prefix
        """
        message = f"[FileIOError] {self.message}"
        if self.context:
            message += f"\nContext: {self.context}"
        if self.original_exception:
            message += f"\nCaused by: {type(self.original_exception).__name__}: {self.original_exception}"
        return message


class ConfigurationError(MedKitError):
    """Exception raised for configuration issues.

    Raised when configuration is missing, invalid, or conflicting.
    This includes missing model configs, invalid settings, etc.

    Example:
        if not config.model:
            raise ConfigurationError(
                "Model configuration is required",
                context="ModelConfig initialization"
            )
    """

    def _format_message(self) -> str:
        """Format configuration error message.

        Returns:
            Formatted error message with Configuration prefix
        """
        message = f"[ConfigurationError] {self.message}"
        if self.context:
            message += f"\nContext: {self.context}"
        if self.original_exception:
            message += f"\nCaused by: {type(self.original_exception).__name__}: {self.original_exception}"
        return message


class MedKitImportError(MedKitError):
    """Exception raised for import failures.

    Raised when required modules or dependencies cannot be imported.

    Example:
        try:
            from some_module import required_class
        except ImportError as e:
            raise MedKitImportError(
                "Required module 'some_module' not found",
                context="Module initialization",
                original_exception=e
            )
    """

    def _format_message(self) -> str:
        """Format import error message.

        Returns:
            Formatted error message with Import prefix
        """
        message = f"[ImportError] {self.message}"
        if self.context:
            message += f"\nContext: {self.context}"
        if self.original_exception:
            message += f"\nCaused by: {type(self.original_exception).__name__}: {self.original_exception}"
        return message


# Export all exception classes
__all__ = [
    "MedKitError",
    "ValidationError",
    "LLMError",
    "FileIOError",
    "ConfigurationError",
    "MedKitImportError",
]
