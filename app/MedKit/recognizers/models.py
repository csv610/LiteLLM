"""
Shared models for recognizers.

This module contains common Pydantic models used across all recognizers.
"""

from typing import Any, Optional

from pydantic import BaseModel, Field


class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""

    data: Optional[Any] = None
    markdown: Optional[str] = None
    metadata: dict = Field(default_factory=dict)
