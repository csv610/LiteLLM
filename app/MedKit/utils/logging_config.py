"""
Centralized logging configuration for the medical module.

This module provides a single source of truth for logging setup,
eliminating duplication across all medical module files.
"""

import logging
from pathlib import Path


def setup_logger(module_name: str, enable_file_handler: bool = True) -> logging.Logger:
    """
    Set up a logger for a module with both file and stream handlers.

    Args:
        module_name: The name of the module (typically __name__)
        enable_file_handler: Whether to add a file handler (default: True)

    Returns:
        A configured logger instance
    """
    # Create logger
    logger = logging.getLogger(module_name)

    # Only configure if not already configured
    if not logger.handlers:
        # Set logging level
        logger.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Add file handler if enabled
        if enable_file_handler:
            # Get the module name from the logger (e.g., "disease_info" from "medkit.medical.disease_info")
            log_filename = module_name.split('.')[-1]
            logs_dir = Path(__file__).parent / "logs"
            logs_dir.mkdir(parents=True, exist_ok=True)
            log_file = logs_dir / f"{log_filename}.log"

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger
