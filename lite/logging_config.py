"""Logging configuration to send all logs to files instead of console."""

import logging
import sys


def configure_logging(
    log_file: str = "litellm.log",
    level: int = logging.INFO,
    enable_console: bool = False,
    verbosity: int = None
):
    """
    Configure logging to output to file instead of console.

    Args:
        log_file: Path to the log file
        level: Logging level (default: logging.INFO)
        enable_console: Whether to also output to console (default: False)
        verbosity: Verbosity level 0-4 (0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG)
                  If provided, overrides the level parameter.
    """
    # Map verbosity level to logging level if provided
    if verbosity is not None:
        verbosity_levels = {
            0: logging.CRITICAL,
            1: logging.ERROR,
            2: logging.WARNING,
            3: logging.INFO,
            4: logging.DEBUG
        }
        level = verbosity_levels.get(verbosity, logging.WARNING)
    # Remove all existing handlers from the root logger
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Configure root logger
    root_logger.setLevel(level)
    root_logger.addHandler(file_handler)

    # Disable console output by removing stream handlers
    logging.disable(logging.NOTSET)

    # Specifically configure LiteLLM logger
    litellm_logger = logging.getLogger("litellm")
    litellm_logger.setLevel(level)

    # Remove any stream handlers from LiteLLM logger
    for handler in litellm_logger.handlers[:]:
        if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
            litellm_logger.removeHandler(handler)

    # Add file handler to LiteLLM logger if it doesn't have one
    if not any(isinstance(h, logging.FileHandler) for h in litellm_logger.handlers):
        litellm_logger.addHandler(file_handler)

    if enable_console:
        # Add console handler if explicitly requested
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
