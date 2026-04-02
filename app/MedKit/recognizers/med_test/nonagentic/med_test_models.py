from typing import Any
"""
medical_test_models.py - Data Models for Medical Test Identification

This module contains Pydantic models used for identifying if a medical test
is well-known in the healthcare field and providing basic information about it.
"""

from typing import Optional

from pydantic import BaseModel, Field


class MedicalTestIdentificationModel(BaseModel):
    """Structured information about a medical test's recognition."""

    test_name: str = Field(description="The name of the medical test being identified")
    is_well_known: bool = Field(
        description="Whether the test is widely recognized in healthcare"
    )
    test_type: str = Field(
        description="The type of test (e.g., blood test, imaging, biopsy, genetic)"
    )
    purpose: str = Field(
        description="What the test is primarily used to detect or monitor"
    )
    clinical_utility: str = Field(
        description="Explanation of its importance in clinical decision making"
    )


class MedicalTestIdentifierModel(BaseModel):
    """
    Comprehensive medical test identification result.
    """

    identification: Optional[MedicalTestIdentificationModel] = Field(
        default=None, description="Detailed identification information"
    )
    summary: str = Field(
        description="A concise summary of the test's status in healthcare"
    )
    data_available: bool = Field(
        description="Whether information about this test was found"
    )


class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
