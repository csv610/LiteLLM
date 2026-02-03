"""
drug_identifier_models.py - Data Models for Drug Identification

This module contains Pydantic models used for identifying if a drug
is well-known in the industry and providing basic information about it.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class DrugIdentificationModel(BaseModel):
    """Structured information about a drug's industry recognition."""
    drug_name: str = Field(description="The name of the drug being identified")
    is_well_known: bool = Field(description="Whether the drug is widely recognized in the pharmaceutical industry")
    common_uses: List[str] = Field(description="List of primary medical conditions this drug is used to treat")
    regulatory_status: str = Field(description="Brief overview of its approval status (e.g., FDA approved, EMA approved)")
    industry_significance: str = Field(description="Explanation of why the drug is or isn't considered well-known")


class DrugIdentifierModel(BaseModel):
    """
    Comprehensive drug identification result.
    """
    identification: Optional[DrugIdentificationModel] = Field(
        default=None,
        description="Detailed identification information"
    )
    summary: str = Field(description="A concise summary of the drug's status in the industry")
    data_available: bool = Field(description="Whether information about this drug was found")


class ModelOutput(BaseModel):
    data: Optional[DrugIdentifierModel] = None
    markdown: Optional[str] = None
