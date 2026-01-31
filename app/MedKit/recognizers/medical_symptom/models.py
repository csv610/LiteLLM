"""
medical_symptom_models.py - Data Models for Medical Symptom Identification

This module contains Pydantic models used for identifying if a medical symptom
is well-known and providing basic clinical information about it.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class MedicalSymptomIdentificationModel(BaseModel):
    """Structured information about a medical symptom's recognition."""
    symptom_name: str = Field(description="The name of the medical symptom being identified")
    is_well_known: bool = Field(description="Whether the symptom is widely recognized in clinical practice")
    associated_conditions: List[str] = Field(description="Common medical conditions or diseases associated with this symptom")
    severity_indicators: str = Field(description="Signs that this symptom might indicate a medical emergency or serious condition")
    clinical_description: str = Field(description="A brief medical description of how the symptom manifests")


class MedicalSymptomIdentifierModel(BaseModel):
    """
    Comprehensive medical symptom identification result.
    """
    identification: Optional[MedicalSymptomIdentificationModel] = Field(
        default=None,
        description="Detailed identification information"
    )
    summary: str = Field(description="A concise summary of the symptom's clinical relevance")
    data_available: bool = Field(description="Whether information about this symptom was found")


class ModelOutput(BaseModel):
    data: Optional[MedicalSymptomIdentifierModel] = None
    markdown: Optional[str] = None
