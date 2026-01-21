"""
Utility modules - Helpers and Tools.

Utilities for prompt generation, privacy compliance, patient history management, and more.
This package also provides base classes and utilities for all MedKit CLI modules
to reduce code duplication and ensure consistent patterns across the codebase.
"""

from .pydantic_prompt_generator import PydanticPromptGenerator, PromptStyle
from .privacy_compliance import PrivacyManager
from .storage_config import StorageConfig

# Base classes for CLI modules
from .base_config import BaseConfig
from .base_generator import BaseGenerator
from .cli_base import (
    setup_logging,
    setup_lite_path,
    get_logger,
    ensure_output_dir,
    get_default_output_path,
)
from .output_formatter import print_result, print_simple_result


__all__ = [
    # Legacy utilities
    "PydanticPromptGenerator",
    "PromptStyle",
    "PrivacyManager",
    "StorageConfig",
    # Base classes for CLI modules
    "BaseConfig",
    "BaseGenerator",
    # CLI utilities
    "setup_logging",
    "setup_lite_path",
    "get_logger",
    "ensure_output_dir",
    "get_default_output_path",
    # Output formatting
    "print_result",
    "print_simple_result",
]
