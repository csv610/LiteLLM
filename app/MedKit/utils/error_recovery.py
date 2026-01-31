"""Error recovery and retry patterns for MedKit.

This module provides decorators and utilities for implementing recovery strategies,
including automatic retries with exponential backoff and fallback handlers.

Usage:
    from utils.error_recovery import RetryableError, FallbackHandler
    from medkit_exceptions import LLMError

    # Use retry decorator
    @RetryableError(max_retries=3, backoff_factor=2)
    def generate_text_with_retry(model_input):
        return client.generate_text(model_input)

    # Use fallback handler
    fallback_handler = FallbackHandler()
    fallback_handler.register("generate_text", fallback_generate_text)
    result = fallback_handler.execute("generate_text", model_input)
"""

import functools
import logging
import time
from typing import Any, Callable, Dict, List

from medkit_exceptions import LLMError, MedKitError


logger = logging.getLogger(__name__)


class RetryableError:
    """Decorator for automatic retry logic with exponential backoff.

    Implements exponential backoff retry strategy for transient failures.
    Useful for handling temporary LLM API failures, network issues, etc.

    Attributes:
        max_retries: Maximum number of retry attempts
        backoff_factor: Multiplier for exponential backoff (default: 2)
        initial_delay: Initial delay in seconds before first retry (default: 1)
        max_delay: Maximum delay between retries in seconds (default: 60)
        retriable_exceptions: Tuple of exceptions to retry on

    Example:
        @RetryableError(max_retries=3, backoff_factor=2)
        def call_llm(model_input):
            return client.generate_text(model_input)

        try:
            result = call_llm(input_data)
        except LLMError as e:
            logger.error(f"Failed after retries: {e}")
    """

    def __init__(
        self,
        max_retries: int = 3,
        backoff_factor: float = 2.0,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        retriable_exceptions: tuple = (LLMError, TimeoutError),
    ):
        """Initialize retry decorator.

        Args:
            max_retries: Maximum number of retry attempts
            backoff_factor: Multiplier for exponential backoff
            initial_delay: Initial delay in seconds
            max_delay: Maximum delay in seconds
            retriable_exceptions: Tuple of exception types to retry on
        """
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.retriable_exceptions = retriable_exceptions

    def __call__(self, func: Callable) -> Callable:
        """Apply retry decorator to function.

        Args:
            func: Function to decorate

        Returns:
            Decorated function with retry logic
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """Wrapper function implementing retry logic.

            Returns:
                Result from function execution
            """
            last_exception = None
            delay = self.initial_delay

            for attempt in range(self.max_retries + 1):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 0:
                        logger.info(f"✓ {func.__name__} succeeded on attempt {attempt + 1}")
                    return result
                except self.retriable_exceptions as e:
                    last_exception = e
                    if attempt < self.max_retries:
                        logger.warning(
                            f"Attempt {attempt + 1}/{self.max_retries + 1} failed for "
                            f"{func.__name__}: {e}. Retrying in {delay:.1f}s..."
                        )
                        time.sleep(delay)
                        # Calculate next delay with exponential backoff
                        delay = min(delay * self.backoff_factor, self.max_delay)
                    else:
                        logger.error(
                            f"All {self.max_retries + 1} attempts failed for {func.__name__}"
                        )

            # All retries exhausted
            if last_exception:
                raise LLMError(
                    f"Failed to execute {func.__name__} after {self.max_retries + 1} attempts",
                    context=f"Last error: {last_exception}",
                    original_exception=last_exception,
                )
            raise LLMError(f"Unexpected failure in {func.__name__}")

        return wrapper


class FallbackHandler:
    """Handler for executing functions with fallback alternatives.

    Allows registration of primary and fallback implementations for operations.
    If the primary implementation fails, automatically attempts fallback implementations.

    Attributes:
        handlers: Dictionary mapping operation names to lists of handlers
        logger: Logger instance

    Example:
        handler = FallbackHandler()
        handler.register("generate", primary_generate)
        handler.register_fallback("generate", fallback_generate)

        result = handler.execute("generate", model_input)
    """

    def __init__(self):
        """Initialize fallback handler."""
        self.handlers: Dict[str, List[Callable]] = {}
        self.logger = logger

    def register(self, operation: str, handler: Callable) -> None:
        """Register a handler for an operation (replaces primary handler).

        Args:
            operation: Operation name
            handler: Handler function to execute
        """
        self.handlers[operation] = [handler]
        self.logger.debug(f"Registered primary handler for operation: {operation}")

    def register_fallback(self, operation: str, handler: Callable) -> None:
        """Register a fallback handler for an operation.

        Args:
            operation: Operation name
            handler: Fallback handler function
        """
        if operation not in self.handlers:
            self.handlers[operation] = []
        self.handlers[operation].append(handler)
        self.logger.debug(f"Registered fallback handler for operation: {operation}")

    def execute(
        self,
        operation: str,
        *args,
        **kwargs
    ) -> Any:
        """Execute operation with fallback handlers.

        Attempts to execute the primary handler, then fallback handlers
        in order until one succeeds.

        Args:
            operation: Operation name
            *args: Positional arguments to pass to handler
            **kwargs: Keyword arguments to pass to handler

        Returns:
            Result from successful handler execution

        Raises:
            MedKitError: If all handlers fail
        """
        if operation not in self.handlers or not self.handlers[operation]:
            raise MedKitError(
                f"No handlers registered for operation: {operation}",
                context="FallbackHandler.execute()"
            )

        handlers = self.handlers[operation]
        last_exception = None

        for attempt, handler in enumerate(handlers):
            handler_name = getattr(handler, "__name__", str(handler))
            is_primary = attempt == 0

            try:
                self.logger.debug(
                    f"Executing {'primary' if is_primary else 'fallback'} handler "
                    f"for {operation}: {handler_name}"
                )
                result = handler(*args, **kwargs)
                if not is_primary:
                    self.logger.info(
                        f"✓ {operation} succeeded using fallback handler: {handler_name}"
                    )
                return result
            except Exception as e:
                last_exception = e
                if is_primary:
                    self.logger.warning(
                        f"Primary handler for {operation} failed: {handler_name}. "
                        f"Error: {e}"
                    )
                    if len(handlers) > 1:
                        self.logger.info(
                            f"Attempting fallback handlers ({len(handlers) - 1} available)..."
                        )
                else:
                    handler_type = f"fallback {attempt}/{len(handlers) - 1}"
                    self.logger.warning(
                        f"{handler_type} handler for {operation} failed: {handler_name}. "
                        f"Error: {e}"
                    )

        # All handlers failed
        self.logger.error(
            f"All {len(handlers)} handler(s) for {operation} failed. "
            f"Last error: {last_exception}"
        )
        raise MedKitError(
            f"All handlers for operation '{operation}' failed",
            context=f"Attempted {len(handlers)} handler(s). Last error: {last_exception}",
            original_exception=last_exception,
        )

    def get_handler_count(self, operation: str) -> int:
        """Get number of registered handlers for an operation.

        Args:
            operation: Operation name

        Returns:
            Number of registered handlers (including primary)
        """
        return len(self.handlers.get(operation, []))

    def list_operations(self) -> List[str]:
        """List all registered operations.

        Returns:
            List of operation names
        """
        return list(self.handlers.keys())

    def clear_operation(self, operation: str) -> None:
        """Clear all handlers for an operation.

        Args:
            operation: Operation name
        """
        if operation in self.handlers:
            del self.handlers[operation]
            self.logger.debug(f"Cleared handlers for operation: {operation}")


class RecoveryStrategy:
    """Base class for error recovery strategies.

    Subclasses can implement custom recovery logic for specific error types.

    Example:
        class LLMRecoveryStrategy(RecoveryStrategy):
            def can_recover(self, error: Exception) -> bool:
                return isinstance(error, LLMError)

            def recover(self, error: Exception, *args, **kwargs) -> Any:
                # Implement recovery logic
                return fallback_result
    """

    def can_recover(self, error: Exception) -> bool:
        """Check if this strategy can handle the error.

        Args:
            error: Exception to check

        Returns:
            True if this strategy can handle the error
        """
        raise NotImplementedError

    def recover(self, error: Exception, *args, **kwargs) -> Any:
        """Attempt to recover from the error.

        Args:
            error: Exception to recover from
            *args: Positional arguments for recovery operation
            **kwargs: Keyword arguments for recovery operation

        Returns:
            Recovery result

        Raises:
            MedKitError: If recovery is not possible
        """
        raise NotImplementedError


__all__ = [
    "RetryableError",
    "FallbackHandler",
    "RecoveryStrategy",
]
