from typing import Any
from typing import Optional

from pydantic import BaseModel, Field


class GeneticVariantIdentificationModel(BaseModel):
    variant_name: str = Field(
        description="Name of the gene or specific mutation (e.g., BRCA1, MTHFR)"
    )
    is_well_known: bool = Field(
        description="Whether the genetic marker is standard in clinical genetics"
    )
    inheritance_pattern: str = Field(
        description="How the variant is typically inherited"
    )
    clinical_implications: str = Field(
        description="Impact on disease risk, diagnosis, or treatment"
    )


class GeneticVariantIdentifierModel(BaseModel):
    identification: Optional[GeneticVariantIdentificationModel] = None
    summary: str = Field(description="Summary of the genetic variant")
    data_available: bool = True


class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
