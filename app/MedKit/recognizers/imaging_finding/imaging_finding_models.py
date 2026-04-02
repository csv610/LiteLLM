from typing import Any
from typing import List, Optional

from pydantic import BaseModel, Field


class ImagingFindingIdentificationModel(BaseModel):
    finding_name: str = Field(
        description="Descriptive name of the imaging finding (e.g., Consolidation)"
    )
    is_well_known: bool = Field(
        description="Whether the term is standard in radiology reporting"
    )
    modalities: List[str] = Field(
        description="Common imaging modalities where this is seen (e.g., CT, X-ray)"
    )
    differential_diagnosis: List[str] = Field(
        description="List of conditions that could present with this finding"
    )


class ImagingFindingIdentifierModel(BaseModel):
    identification: Optional[ImagingFindingIdentificationModel] = None
    summary: str = Field(description="Summary of the imaging finding")
    data_available: bool = True


class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
