from typing import Any
"""Pydantic models for medical label information structure."""

from typing import Optional

from pydantic import BaseModel, Field


class MedicalLabelInfoModel(BaseModel):
    """
    Simplified medical label information.
    """

    term: str = Field(description="The medical term being explained")
    explanation: str = Field(
        description="A 100-200 word explanation emphasizing the functionality and medical importance of the term"
    )


class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
