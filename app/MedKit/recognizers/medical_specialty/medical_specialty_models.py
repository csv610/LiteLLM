"""
medical_specialty_models.py - Data Models for Medical Specialty Identification

This module contains Pydantic models used for identifying if a medical specialty
is well-known and providing basic information about its scope.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class MedicalSpecialtyIdentificationModel(BaseModel):
    """Structured information about a medical specialty's recognition."""
    specialty_name: str = Field(description="The name of the medical specialty being identified")
    is_well_known: bool = Field(description="Whether the specialty is widely recognized in medicine")
    organs_treated: List[str] = Field(description="Major organs or body systems this specialty focuses on")
    common_procedures: List[str] = Field(description="Common medical or surgical procedures performed by specialists in this field")
    clinical_scope: str = Field(description="A brief description of the types of conditions and patients this specialty manages")


class MedicalSpecialtyIdentifierModel(BaseModel):
    """
    Comprehensive medical specialty identification result.
    """
    identification: Optional[MedicalSpecialtyIdentificationModel] = Field(
        default=None,
        description="Detailed identification information"
    )
    summary: str = Field(description="A concise summary of the specialty's role in healthcare")
    data_available: bool = Field(description="Whether information about this specialty was found")


class ModelOutput(BaseModel):
    data: Optional[MedicalSpecialtyIdentifierModel] = None
    markdown: Optional[str] = None
