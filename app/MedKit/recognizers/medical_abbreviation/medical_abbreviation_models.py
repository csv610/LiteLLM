"""
medical_abbreviation_models.py - Data Models for Medical Abbreviation Identification

This module contains Pydantic models used for identifying and expanding
medical abbreviations and clinical shorthand.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class AbbreviationIdentificationModel(BaseModel):
    """Structured information about a medical abbreviation's expansion."""
    abbreviation: str = Field(description="The medical abbreviation being identified")
    full_form: str = Field(description="The expanded, full medical term")
    is_well_known: bool = Field(description="Whether the abbreviation is standard in medical practice")
    context_of_use: str = Field(description="Typical context where this is used (e.g., prescriptions, physical exams)")
    clinical_meaning: str = Field(description="A brief explanation of what the term represents clinically")


class AbbreviationIdentifierModel(BaseModel):
    """
    Comprehensive medical abbreviation identification result.
    """
    identification: Optional[AbbreviationIdentificationModel] = Field(
        default=None,
        description="Detailed identification information"
    )
    summary: str = Field(description="A concise summary of the abbreviation's usage")
    data_available: bool = Field(description="Whether information about this abbreviation was found")


class ModelOutput(BaseModel):
    data: Optional[AbbreviationIdentifierModel] = None
    markdown: Optional[str] = None
