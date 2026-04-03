from typing import Any

"""Pydantic models for medical label information structure."""

from typing import Optional
from lite import ModelOutput
from pydantic import BaseModel, Field


class MedicalLabelInfoModel(BaseModel):
    """
    Simplified medical label information.
    """

    term: str = Field(description="The medical term being explained")
    explanation: str = Field(
        description="A 100-200 word explanation emphasizing the functionality and medical importance of the term"
    )
