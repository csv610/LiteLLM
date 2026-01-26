"""
Utility modules - Helpers and Tools.

Utilities for prompt generation, privacy compliance, patient history management, and more.
This package also provides base classes and utilities for all MedKit CLI modules
to reduce code duplication and ensure consistent patterns across the codebase.
"""

from .pydantic_prompt_generator import PydanticPromptGenerator, PromptStyle
from .privacy_compliance import PrivacyManager
from .storage_config import StorageConfig

# Base classes for CLI modules - imported only if available
try:
    from .cli_base import (
        setup_logging,
        setup_lite_path,
        get_logger,
        ensure_output_dir,
        get_default_output_path,
    )
except ImportError:
    # Fallback empty implementations for compatibility
    def setup_logging(*args, **kwargs):
        pass
    def setup_lite_path(*args, **kwargs):
        pass
    def get_logger(*args, **kwargs):
        import logging
        return logging.getLogger(__name__)
    def ensure_output_dir(*args, **kwargs):
        pass
    def get_default_output_path(*args, **kwargs):
        return None

from .output_formatter import print_result, print_simple_result

# Legacy base classes - not imported by default to avoid circular imports
# BaseConfig = None
# BaseGenerator = None


__all__ = [
    # Legacy utilities
    "PydanticPromptGenerator",
    "PromptStyle",
    "PrivacyManager",
    "StorageConfig",
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
