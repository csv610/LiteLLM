"""
millennium_prize_models.py - Pydantic models for Millennium Prize Problems

Defines data models for representing Millennium Prize Problems with their
status, solvers, and detailed information about each problem.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class MillenniumProblem(BaseModel):
    """Represents a Millennium Prize Problem."""
    title: str = Field(..., description="The official name of problem")
    description: str = Field(..., description="Detailed explanation of problem")
    field: str = Field(..., description="The mathematical or physics field problem belongs to")
    status: str = Field(..., description="Current status (Unsolved or Solved)")
    solver: Optional[str] = Field(None, description="Name of solver if problem has been solved")
    year_solved: Optional[int] = Field(None, description="Year problem was solved")
    significance: str = Field(..., description="Why this problem is important and its implications")
    current_progress: str = Field(..., description="Recent progress, approaches, or partial results")


class MillenniumProblemsResponse(BaseModel):
    """Response containing a list of Millennium Prize Problems."""
    total_problems: int = Field(..., description="Total number of Millennium Prize Problems")
    problems: List[MillenniumProblem]
