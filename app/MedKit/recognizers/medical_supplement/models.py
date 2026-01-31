"""
medical_supplement_models.py - Data Models for Supplement Identification

This module contains Pydantic models used for identifying dietary supplements,
vitamins, and minerals.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class SupplementIdentificationModel(BaseModel):
    """Structured information about a dietary supplement."""
    supplement_name: str = Field(description="The name of the supplement (e.g., Vitamin D3, Ashwagandha)")
    is_well_known: bool = Field(description="Whether the supplement is widely recognized in health and wellness")
    primary_nutrients: List[str] = Field(description="Key active ingredients or nutrients")
    common_uses: List[str] = Field(description="Primary reasons people take this supplement")
    regulatory_standing: str = Field(description="Brief overview of its regulatory status (e.g., FDA regulated as food)")


class SupplementIdentifierModel(BaseModel):
    """
    Comprehensive supplement identification result.
    """
    identification: Optional[SupplementIdentificationModel] = Field(
        default=None,
        description="Detailed identification information"
    )
    summary: str = Field(description="A concise summary of the supplement")
    data_available: bool = Field(description="Whether information about this supplement was found")


class ModelOutput(BaseModel):
    data: Optional[SupplementIdentifierModel] = None
    markdown: Optional[str] = None
