"""
medical_anatomy_models.py - Data Models for Medical Anatomy Identification

This module contains Pydantic models used for identifying if an anatomical structure
is well-known in the medical field and providing basic information about it.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class MedicalAnatomyIdentificationModel(BaseModel):
    """Structured information about an anatomical structure's recognition."""
    structure_name: str = Field(description="The name of the anatomical structure being identified")
    is_well_known: bool = Field(description="Whether the structure is widely recognized in anatomy and medicine")
    system: str = Field(description="The primary body system it belongs to (e.g., cardiovascular, nervous, skeletal)")
    location: str = Field(description="General anatomical location in the body")
    clinical_significance: str = Field(description="Explanation of its importance in clinical practice, surgery, or pathology")


class MedicalAnatomyIdentifierModel(BaseModel):
    """
    Comprehensive medical anatomy identification result.
    """
    identification: Optional[MedicalAnatomyIdentificationModel] = Field(
        default=None,
        description="Detailed identification information"
    )
    summary: str = Field(description="A concise summary of the structure's status in anatomy")
    data_available: bool = Field(description="Whether information about this structure was found")


class ModelOutput(BaseModel):
    data: Optional[MedicalAnatomyIdentifierModel] = None
    markdown: Optional[str] = None
