from typing import Any
"""
Pydantic models for surgical tray information structure.

This module defines the data models used to represent comprehensive surgical tray
and instrument information with validation and structured schema generation.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class TrayInstrument(BaseModel):
    name: str = Field(description="Name of the instrument")
    quantity: int = Field(description="Typical quantity required")
    category: str = Field(description="Category (e.g., Scalpel, Forceps, Retractor)")
    reason: str = Field(description="Why this instrument is needed for this surgery")


class SurgicalTrayModel(BaseModel):
    surgery_name: str = Field(description="Name of the surgery")
    specialty: str = Field(description="Surgical specialty")
    instruments: List[TrayInstrument] = Field(
        description="List of instruments in the tray"
    )
    sterilization_method: str = Field(
        description="Recommended sterilization method for the whole tray"
    )
    setup_instructions: str = Field(
        description="Brief setup instructions for the scrub nurse"
    )


class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
