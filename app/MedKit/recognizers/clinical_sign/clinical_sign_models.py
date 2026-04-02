from typing import Any
from typing import Optional

from pydantic import BaseModel, Field


class ClinicalSignIdentificationModel(BaseModel):
    sign_name: str = Field(
        description="Name of the clinical sign (e.g., Babinski sign)"
    )
    is_well_known: bool = Field(
        description="Whether the sign is a standard part of clinical examination"
    )
    examination_method: str = Field(
        description="How the sign is elicited or observed during a physical exam"
    )
    clinical_significance: str = Field(
        description="What a positive or negative finding typically indicates"
    )


class ClinicalSignIdentifierModel(BaseModel):
    identification: Optional[ClinicalSignIdentificationModel] = None
    summary: str = Field(description="Summary of the clinical sign")
    data_available: bool = True


class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
