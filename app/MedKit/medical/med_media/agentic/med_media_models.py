from typing import Any
from typing import List, Optional

from pydantic import BaseModel, Field


class MediaCaptionModel(BaseModel):
    """AI generated caption for medical media."""

    title: str = Field(description="Short descriptive title for the media")
    caption: str = Field(
        description="Comprehensive medical caption describing the media"
    )
    key_entities: List[str] = Field(
        description="Key medical entities visible or discussed (anatomy, pathology, tools)"
    )
    clinical_context: str = Field(
        description="Typical clinical context where this media would be relevant"
    )


class MediaSummaryModel(BaseModel):
    """AI generated summary for medical media or topic."""

    topic: str = Field(description="The main medical topic of the media")
    summary: str = Field(
        description="A concise summary of the key information presented"
    )
    clinical_significance: str = Field(
        description="The medical or clinical importance of the topic"
    )
    target_audience: str = Field(
        description="Recommended audience (Student, Resident, Specialist, Patient)"
    )


class MedicalMediaModel(BaseModel):
    """Combined media analysis model."""

    caption: Optional[MediaCaptionModel] = None
    summary: Optional[MediaSummaryModel] = None


class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
