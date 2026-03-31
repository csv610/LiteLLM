"""
Pydantic models for Hilbert's 23 Problems reference guide.
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class ProblemStatus(str, Enum):
    """Status of Hilbert problems."""
    SOLVED = "solved"
    UNSOLVED = "unsolved"
    PARTIALLY_SOLVED = "partially_solved"


class HilbertProblemModel(BaseModel):
    """Structured data for a Hilbert problem."""
    number: int = Field(description="Problem number (1-23)")
    title: str = Field(description="Title of the problem")
    description: str = Field(description="Mathematical description of the problem")
    status: ProblemStatus = Field(description="Current status of the problem")
    solved_by: Optional[str] = Field(description="Mathematician(s) who solved it")
    solution_year: Optional[int] = Field(description="Year the problem was solved")
    solution_method: str = Field(description="Detailed explanation of the solution method")
    related_fields: List[str] = Field(description="Related mathematical fields")
    notes: str = Field(description="Additional notes and implications")
