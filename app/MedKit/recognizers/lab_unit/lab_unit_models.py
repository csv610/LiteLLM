from pydantic import BaseModel, Field
from typing import Optional, List

class LabUnitIdentificationModel(BaseModel):
    unit_name: str = Field(description="The unit abbreviation or name (e.g., mEq/L)")
    is_well_known: bool = Field(description="Whether the unit is standard in laboratory medicine")
    category: str = Field(description="What the unit measures (e.g., concentration, mass, enzymatic activity)")
    common_tests: List[str] = Field(description="Medical tests that typically use this unit")

class LabUnitIdentifierModel(BaseModel):
    identification: Optional[LabUnitIdentificationModel] = None
    summary: str = Field(description="Summary of the lab unit")
    data_available: bool = True

class ModelOutput(BaseModel):
    data: Optional[LabUnitIdentifierModel] = None
    markdown: Optional[str] = None
