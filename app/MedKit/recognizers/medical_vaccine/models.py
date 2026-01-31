"""
medical_vaccine_models.py - Data Models for Vaccine Identification

This module contains Pydantic models used for identifying and describing
vaccines and immunization agents.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class VaccineIdentificationModel(BaseModel):
    """Structured information about a vaccine."""
    vaccine_name: str = Field(description="The name of the vaccine (e.g., MMR, BCG, Pfizer-BioNTech COVID-19)")
    is_well_known: bool = Field(description="Whether the vaccine is widely recognized in public health")
    target_diseases: List[str] = Field(description="Diseases the vaccine is designed to prevent")
    vaccine_type: str = Field(description="Type of vaccine (e.g., mRNA, Live-attenuated, Inactivated, Subunit)")
    standard_schedule: str = Field(description="Typical administration schedule or age group")


class VaccineIdentifierModel(BaseModel):
    """
    Comprehensive vaccine identification result.
    """
    identification: Optional[VaccineIdentificationModel] = Field(
        default=None,
        description="Detailed identification information"
    )
    summary: str = Field(description="A concise summary of the vaccine")
    data_available: bool = Field(description="Whether information about this vaccine was found")


class ModelOutput(BaseModel):
    data: Optional[VaccineIdentifierModel] = None
    markdown: Optional[str] = None
