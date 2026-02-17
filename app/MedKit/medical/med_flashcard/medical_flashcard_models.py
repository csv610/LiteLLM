"""Pydantic models for medical label information structure."""

from pydantic import BaseModel, Field
from typing import Optional

class MedicalLabelInfoModel(BaseModel):
    """
    Simplified medical label information.
    """
    term: str = Field(description="The medical term being explained")
    explanation: str = Field(description="A 100-200 word explanation emphasizing the functionality and medical importance of the term")


class ModelOutput(BaseModel):
    data: Optional[MedicalLabelInfoModel] = None
    markdown: Optional[str] = None
