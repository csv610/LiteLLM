"""
medical_condition_models.py - Data Models for Medical Condition Identification

This module contains Pydantic models used for identifying if a medical condition
is well-known in the healthcare field and providing basic information about it.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class MedicalConditionIdentificationModel(BaseModel):
    """Structured information about a medical condition's recognition."""
    condition_name: str = Field(description="The name of the medical condition being identified")
    is_well_known: bool = Field(description="Whether the condition is widely recognized in healthcare")
    category: str = Field(description="The category of the condition (e.g., chronic, acute, genetic, injury)")
    key_characteristics: List[str] = Field(description="List of primary signs, symptoms, or features of this condition")
    clinical_significance: str = Field(description="Explanation of its importance in clinical practice and patient care")


class MedicalConditionIdentifierModel(BaseModel):
    """
    Comprehensive medical condition identification result.
    """
    identification: Optional[MedicalConditionIdentificationModel] = Field(
        default=None,
        description="Detailed identification information"
    )
    summary: str = Field(description="A concise summary of the condition's status in healthcare")
    data_available: bool = Field(description="Whether information about this condition was found")


class ModelOutput(BaseModel):
    data: Optional[MedicalConditionIdentifierModel] = None
    markdown: Optional[str] = None
