"""Base utilities for CLI modules in MedKit.

This module provides common utilities for logging configuration, path setup,
and other shared functionality across all MedKit CLI modules.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# Import centralized logging configuration
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.logging_config import configure_logging


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
