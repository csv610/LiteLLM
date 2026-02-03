"""
medication_class_models.py - Data Models for Medication Class Identification

This module contains Pydantic models used for identifying and describing
classes of medications.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class MedicationClassIdentificationModel(BaseModel):
    """Structured information about a medication class."""
    class_name: str = Field(description="The name of the medication class (e.g., SSRIs, Statins)")
    is_well_known: bool = Field(description="Whether the class is widely recognized in pharmacology")
    mechanism_of_action: str = Field(description="How medications in this class typically work in the body")
    common_examples: List[str] = Field(description="Common drug names that belong to this class")
    therapeutic_uses: List[str] = Field(description="Primary medical conditions treated by this class")


class MedicationClassIdentifierModel(BaseModel):
    """
    Comprehensive medication class identification result.
    """
    identification: Optional[MedicationClassIdentificationModel] = Field(
        default=None,
        description="Detailed identification information"
    )
    summary: str = Field(description="A concise summary of the medication class")
    data_available: bool = Field(description="Whether information about this class was found")


class ModelOutput(BaseModel):
    data: Optional[MedicationClassIdentifierModel] = None
    markdown: Optional[str] = None
