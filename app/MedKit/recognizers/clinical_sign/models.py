from pydantic import BaseModel, Field
from typing import Optional, List

class ClinicalSignIdentificationModel(BaseModel):
    sign_name: str = Field(description="Name of the clinical sign (e.g., Babinski sign)")
    is_well_known: bool = Field(description="Whether the sign is a standard part of clinical examination")
    examination_method: str = Field(description="How the sign is elicited or observed during a physical exam")
    clinical_significance: str = Field(description="What a positive or negative finding typically indicates")

class ClinicalSignIdentifierModel(BaseModel):
    identification: Optional[ClinicalSignIdentificationModel] = None
    summary: str = Field(description="Summary of the clinical sign")
    data_available: bool = True

class ModelOutput(BaseModel):
    data: Optional[ClinicalSignIdentifierModel] = None
    markdown: Optional[str] = None
