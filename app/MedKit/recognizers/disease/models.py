"""
disease_identifier_models.py - Data Models for Disease Identification

This module contains Pydantic models used for identifying if a disease
is well-known in the medical field and providing basic information about it.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class DiseaseIdentificationModel(BaseModel):
    """Structured information about a disease's medical recognition."""
    disease_name: str = Field(description="The name of the disease being identified")
    is_well_known: bool = Field(description="Whether the disease is widely recognized in the medical community")
    common_symptoms: List[str] = Field(description="List of primary symptoms associated with this disease")
    prevalence: str = Field(description="General information about how common the disease is (e.g., rare, common, epidemic)")
    medical_significance: str = Field(description="Explanation of its impact on public health or clinical practice")


class DiseaseIdentifierModel(BaseModel):
    """
    Comprehensive disease identification result.
    """
    identification: Optional[DiseaseIdentificationModel] = Field(
        default=None,
        description="Detailed identification information"
    )
    summary: str = Field(description="A concise summary of the disease's status in medicine")
    data_available: bool = Field(description="Whether information about this disease was found")


class ModelOutput(BaseModel):
    data: Optional[DiseaseIdentifierModel] = None
    markdown: Optional[str] = None
