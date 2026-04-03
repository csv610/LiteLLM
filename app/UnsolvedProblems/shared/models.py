"""
unsolved_problems_models.py - Pydantic models for unsolved problems.

Defines request and response schemas used by the generation and review agents.
"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from lite import ModelOutput


class UnsolvedProblem(BaseModel):
    """Represents an unsolved problem in a given field."""

    title: str = Field(..., description="The name or title of the unsolved problem")
    description: str = Field(
        ..., description="Brief description of the problem and why it's important"
    )
    field: str = Field(
        ..., description="The specific field or subfield the problem belongs to"
    )
    difficulty: str = Field(
        ...,
        description="Estimated difficulty level (Elementary, Moderate, or Advanced)",
    )
    first_posed: Optional[str] = Field(
        None, description="When or by whom the problem was first posed, if known"
    )
    prize_money: Optional[str] = Field(
        None,
        description="Any prize money associated with solving this problem, if applicable",
    )
    significance: str = Field(
        ..., description="Why solving this problem would be significant for the field"
    )
    current_status: str = Field(
        ..., description="The best known results or current status as of today"
    )


class UnsolvedProblemsResponse(BaseModel):
    """Structured response returned by the research agent."""

    topic: str = Field(..., description="The requested topic")
    problems: List[UnsolvedProblem] = Field(
        ..., description="Structured list of unsolved problems for the topic"
    )


class ReviewedUnsolvedProblemsResponse(BaseModel):
    """Structured response returned by the review agent."""

    topic: str = Field(..., description="The requested topic")
    problems: List[UnsolvedProblem] = Field(
        ...,
        description="Reviewed and normalized list of unsolved problems after quality checks",
    )


class ProblemStatus(str, Enum):
    UNSOLVED = "unsolved"
    OPEN = "open"
    PARTIALLY_SOLVED = "partially_solved"


class UnsolvedProblemModel(BaseModel):
    title: str
    category: str
    description: str
    status: ProblemStatus
    importance: str
    related_fields: List[str] = Field(default_factory=list)


UnsolvedProblemResponse = UnsolvedProblemsResponse
