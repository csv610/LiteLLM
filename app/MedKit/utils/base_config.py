"""Base configuration class for all MedKit CLI modules.

This module provides the base configuration dataclass that all CLI modules
should inherit from to ensure consistent configuration patterns.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class BaseConfig:
    """Base configuration for all MedKit CLI generators.

    Attributes:
        output_path: Optional specific path to save the output file
        output_dir: Directory for output files (default: outputs)
        verbosity: Logging verbosity level (0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG)
        enable_cache: Enable caching for API calls
    """
    output_path: Optional[Path] = None
    output_dir: Path = Path("outputs")
    verbosity: int = 2  # Default to WARNING level
    enable_cache: bool = True
