"""
medical_procedure_models.py - Data Models for Medical Procedure Identification

This module contains Pydantic models used for identifying if a medical procedure
is well-known in the healthcare field and providing basic information about it.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class MedicalProcedureIdentificationModel(BaseModel):
    """Structured information about a medical procedure's recognition."""
    procedure_name: str = Field(description="The name of the medical procedure being identified")
    is_well_known: bool = Field(description="Whether the procedure is widely recognized in healthcare")
    procedure_type: str = Field(description="The type of procedure (e.g., surgical, diagnostic, therapeutic, minimally invasive)")
    indications: List[str] = Field(description="Primary medical reasons or conditions for which this procedure is performed")
    clinical_significance: str = Field(description="Explanation of its importance in patient treatment or diagnosis")


class MedicalProcedureIdentifierModel(BaseModel):
    """
    Comprehensive medical procedure identification result.
    """
    identification: Optional[MedicalProcedureIdentificationModel] = Field(
        default=None,
        description="Detailed identification information"
    )
    summary: str = Field(description="A concise summary of the procedure's status in healthcare")
    data_available: bool = Field(description="Whether information about this procedure was found")


class ModelOutput(BaseModel):
    data: Optional[MedicalProcedureIdentifierModel] = None
    markdown: Optional[str] = None
