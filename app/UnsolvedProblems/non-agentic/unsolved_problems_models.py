"""
unsolved_problems_models.py - Pydantic models for unsolved problems

Defines data models for representing unsolved problems in various academic fields
with their status, significance, and detailed information.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class UnsolvedProblem(BaseModel):
    """Represents an unsolved problem in a given field."""
    title: str = Field(..., description="The name or title of the unsolved problem")
    description: str = Field(..., description="Brief description of the problem and why it's important")
    field: str = Field(..., description="The specific field or subfield the problem belongs to")
    difficulty: str = Field(..., description="Estimated difficulty level (Elementary, Moderate, or Advanced)")
    first_posed: Optional[str] = Field(None, description="When or by whom the problem was first posed, if known")
    prize_money: Optional[str] = Field(None, description="Any prize money associated with solving this problem, if applicable")
    significance: str = Field(..., description="Why solving this problem would be significant for the field")
    current_status: str = Field(..., description="The best known results or current status as of today")


class UnsolvedProblemsModel(BaseModel):
    """Response containing a list of unsolved problems."""
    topic: str = Field(..., description="The topic for which unsolved problems are listed")
    problems: List[UnsolvedProblem]
