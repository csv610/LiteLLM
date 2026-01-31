"""
medical_test_models.py - Data Models for Medical Test Identification

This module contains Pydantic models used for identifying if a medical test
is well-known in the healthcare field and providing basic information about it.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class MedicalTestIdentificationModel(BaseModel):
    """Structured information about a medical test's recognition."""
    test_name: str = Field(description="The name of the medical test being identified")
    is_well_known: bool = Field(description="Whether the test is widely recognized in healthcare")
    test_type: str = Field(description="The type of test (e.g., blood test, imaging, biopsy, genetic)")
    purpose: str = Field(description="What the test is primarily used to detect or monitor")
    clinical_utility: str = Field(description="Explanation of its importance in clinical decision making")


class MedicalTestIdentifierModel(BaseModel):
    """
    Comprehensive medical test identification result.
    """
    identification: Optional[MedicalTestIdentificationModel] = Field(
        default=None,
        description="Detailed identification information"
    )
    summary: str = Field(description="A concise summary of the test's status in healthcare")
    data_available: bool = Field(description="Whether information about this test was found")


class ModelOutput(BaseModel):
    data: Optional[MedicalTestIdentifierModel] = None
    markdown: Optional[str] = None
