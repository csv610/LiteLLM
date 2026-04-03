from typing import Any

"""
med_images_models.py - Pydantic models for med image classification

Defines the data structures used for medical image classification.
"""

from typing import Optional

from lite import ModelOutput


class MedicalImageClassificationModel(BaseModel):
    """Model for short medical image classification results."""

    modality: str = Field(
        description="The medical imaging modality (X-Ray, CT-Scan, etc)."
    )
    anatomical_site: str = Field(description="The body part or organ being imaged.")
    classification: str = Field(description="The primary classification or finding.")
    confidence_score: float = Field(description="Confidence score (0.0 to 1.0).")
