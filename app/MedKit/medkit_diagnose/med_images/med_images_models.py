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
    data: Optional[MedicalImageClassificationModel] = None
    markdown: Optional[str] = None

    @model_validator(mode="after")
    def check_exactly_one(self) -> "ModelOutput":
        if (self.data is None) == (self.markdown is None):
            raise ValueError("Exactly one of 'data' or 'markdown' must be set")
        return self
