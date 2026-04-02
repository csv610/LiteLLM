from typing import Any
"""Pydantic models for primary health care response structure."""

from typing import List, Optional

from pydantic import BaseModel, Field


class PrimaryCareResponseModel(BaseModel):
    """
    Structured response from a primary health care provider.
    """

    understanding_concern: str = Field(
        description="A brief summary of the patient's concern or the topic"
    )
    common_symptoms: List[str] = Field(
        description="List of common symptoms or observations related to the query"
    )
    general_explanation: str = Field(
        description="Accessible explanation of the condition or health topic"
    )
    self_care_advice: str = Field(
        description="General advice and practical self-care steps"
    )
    when_to_seek_care: str = Field(
        description="Clear indicators for when to seek professional or urgent medical attention"
    )
    next_steps: List[str] = Field(
        description="Recommended next steps or questions for a follow-up appointment"
    )


class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
