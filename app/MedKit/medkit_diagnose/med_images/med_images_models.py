from typing import Any
"""
med_images_models.py - Pydantic models for med image classification

Defines the data structures used for medical image classification.
"""

from typing import Optional

from pydantic import BaseModel, Field, model_validator


class MedicalImageClassificationModel(BaseModel):
    """Model for short medical image classification results."""

    modality: str = Field(
        description="The medical imaging modality (X-Ray, CT-Scan, etc)."
    )
    anatomical_site: str = Field(description="The body part or organ being imaged.")
    classification: str = Field(description="The primary classification or finding.")
    confidence_score: float = Field(description="Confidence score (0.0 to 1.0).")


class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
