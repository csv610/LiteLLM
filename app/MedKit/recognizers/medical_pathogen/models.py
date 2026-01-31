"""
medical_pathogen_models.py - Data Models for Pathogen Identification

This module contains Pydantic models used for identifying and describing
pathogenic microorganisms.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class PathogenIdentificationModel(BaseModel):
    """Structured information about a pathogen."""
    pathogen_name: str = Field(description="The scientific or common name of the pathogen")
    is_well_known: bool = Field(description="Whether the pathogen is widely recognized in medicine")
    pathogen_type: str = Field(description="Type of pathogen (e.g., bacteria, virus, fungus, parasite)")
    associated_infections: List[str] = Field(description="Infections or diseases caused by this pathogen")
    clinical_significance: str = Field(description="Brief explanation of its impact on health and treatment approach")


class PathogenIdentifierModel(BaseModel):
    """
    Comprehensive pathogen identification result.
    """
    identification: Optional[PathogenIdentificationModel] = Field(
        default=None,
        description="Detailed identification information"
    )
    summary: str = Field(description="A concise summary of the pathogen")
    data_available: bool = Field(description="Whether information about this pathogen was found")


class ModelOutput(BaseModel):
    data: Optional[PathogenIdentifierModel] = None
    markdown: Optional[str] = None
