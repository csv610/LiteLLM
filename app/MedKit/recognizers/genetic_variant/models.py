from pydantic import BaseModel, Field
from typing import Optional, List

class GeneticVariantIdentificationModel(BaseModel):
    variant_name: str = Field(description="Name of the gene or specific mutation (e.g., BRCA1, MTHFR)")
    is_well_known: bool = Field(description="Whether the genetic marker is standard in clinical genetics")
    inheritance_pattern: str = Field(description="How the variant is typically inherited")
    clinical_implications: str = Field(description="Impact on disease risk, diagnosis, or treatment")

class GeneticVariantIdentifierModel(BaseModel):
    identification: Optional[GeneticVariantIdentificationModel] = None
    summary: str = Field(description="Summary of the genetic variant")
    data_available: bool = True

class ModelOutput(BaseModel):
    data: Optional[GeneticVariantIdentifierModel] = None
    markdown: Optional[str] = None
