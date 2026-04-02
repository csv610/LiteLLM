from typing import Any
from typing import List, Optional

from pydantic import BaseModel, Field


class LabUnitIdentificationModel(BaseModel):
    unit_name: str = Field(description="The unit abbreviation or name (e.g., mEq/L)")
    is_well_known: bool = Field(
        description="Whether the unit is standard in laboratory medicine"
    )
    category: str = Field(
        description="What the unit measures (e.g., concentration, mass, enzymatic activity)"
    )
    common_tests: List[str] = Field(
        description="Medical tests that typically use this unit"
    )


class LabUnitIdentifierModel(BaseModel):
    identification: Optional[LabUnitIdentificationModel] = None
    summary: str = Field(description="Summary of the lab unit")
    data_available: bool = True


class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
