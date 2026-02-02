"""
Pydantic models for surgical tray information structure.

This module defines the data models used to represent comprehensive surgical tray
and instrument information with validation and structured schema generation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class TrayInstrument(BaseModel):
    name: str = Field(description="Name of the instrument")
    quantity: int = Field(description="Typical quantity required")
    category: str = Field(description="Category (e.g., Scalpel, Forceps, Retractor)")
    reason: str = Field(description="Why this instrument is needed for this surgery")


class SurgicalTrayModel(BaseModel):
    surgery_name: str = Field(description="Name of the surgery")
    specialty: str = Field(description="Surgical specialty")
    instruments: List[TrayInstrument] = Field(description="List of instruments in the tray")
    sterilization_method: str = Field(description="Recommended sterilization method for the whole tray")
    setup_instructions: str = Field(description="Brief setup instructions for the scrub nurse")


class ModelOutput(BaseModel):
    tray_data: Optional[SurgicalTrayModel] = None
    markdown: Optional[str] = None