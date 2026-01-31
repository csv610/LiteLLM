from pydantic import BaseModel, Field
from typing import Optional, List

class MedicalCodingIdentificationModel(BaseModel):
    system_name: str = Field(description="Name of the coding system (e.g., ICD-10, CPT)")
    is_well_known: bool = Field(description="Whether the system is widely used for medical billing or documentation")
    purpose: str = Field(description="The primary use of the system (e.g., diagnosis codes, procedure codes)")
    governing_body: str = Field(description="Organization that maintains the coding system")

class MedicalCodingIdentifierModel(BaseModel):
    identification: Optional[MedicalCodingIdentificationModel] = None
    summary: str = Field(description="Summary of the coding system")
    data_available: bool = True

class ModelOutput(BaseModel):
    data: Optional[MedicalCodingIdentifierModel] = None
    markdown: Optional[str] = None
