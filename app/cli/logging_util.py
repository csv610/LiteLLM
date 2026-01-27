"""
Centralized logging configuration for CLI modules.

This module provides a unified logging setup to avoid duplication across
multiple CLI scripts. It configures logging with both file and optional
console handlers.
"""

import logging
import os
from pathlib import Path
from typing import Optional


def setup_logging(
    log_file: str,
    include_console: bool = False,
    log_level: int = logging.INFO
) -> logging.Logger:
    """
    Configure logging with file handler and optional console output.

    Args:
        log_file: Path to log file
        include_console: Whether to include console (StreamHandler) output
        log_level: Logging level (default: logging.INFO)

    Returns:
        Configured logger instance

    Example:
        >>> logger = setup_logging('my_app.log', include_console=True)
        >>> logger.info("Application started")
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicates when called multiple times
    logger.handlers.clear()

    # Create logs directory if it doesn't exist
    log_path = Path(log_file)
    if len(log_path.parts) == 1:
        log_path = Path("logs") / log_path
        log_file = str(log_path)

    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Common formatter for all handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler (always included)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Set restrictive file permissions (owner read/write only)
    try:
        os.chmod(log_file, 0o600)
    except OSError:
        pass  # File may not exist yet, permissions will be set on first write

    # Optional console handler
    if include_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger by name.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
