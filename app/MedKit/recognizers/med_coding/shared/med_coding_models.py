from typing import Any
from typing import Optional

from pydantic import BaseModel, Field


class MedicalCodingIdentificationModel(BaseModel):
    system_name: str = Field(
        description="Name of the coding system (e.g., ICD-10, CPT)"
    )
    is_well_known: bool = Field(
        description="Whether the system is widely used for medical billing or documentation"
    )
    purpose: str = Field(
        description="The primary use of the system (e.g., diagnosis codes, procedure codes)"
    )
    governing_body: str = Field(
        description="Organization that maintains the coding system"
    )


class MedicalCodingIdentifierModel(BaseModel):
    identification: Optional[MedicalCodingIdentificationModel] = None
    summary: str = Field(description="Summary of the coding system")
    data_available: bool = True


class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
