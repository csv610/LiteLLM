"""
scholar_work_models.py - Pydantic models for scholar major works

Defines data models for generating and storing narrative-driven explanations
of major scientific work done by a given scientist.
"""

from pydantic import BaseModel, Field
from typing import List


class ResearchBrief(BaseModel):
    """A detailed research brief about a scholar's major work."""
    scholar_name: str = Field(..., description="The name of the scholar")
    major_contribution: str = Field(..., description="The name of the specific work or breakthrough")
    historical_context: str = Field(..., description="The scientific and social landscape during the time of discovery")
    scientific_core: str = Field(..., description="The fundamental scientific principles and logic behind the discovery")
    revolutionary_impact: str = Field(..., description="How this work changed existing paradigms or understanding")
    modern_legacy: List[str] = Field(..., description="3-5 concrete ways this work influences science or society today")
    key_anecdotes: List[str] = Field(..., description="Potential human-interest stories or anecdotes related to the discovery")


class ScholarMajorWork(BaseModel):
    """A coherent narrative story explaining a major work by a scholar"""
    scholar_name: str = Field(..., description="Name of the scholar being described")
    major_contribution: str = Field(..., description="The main scientific contribution or theory being explained")
    title: str = Field(..., description="An engaging title for the story")
    subtitle: str = Field(..., description="A compelling subtitle or subheading")

    # The complete narrative - a flowing story, not fragmented sections
    story: str = Field(..., description="The complete narrative story as flowing prose, written like a professional science article")

    # Supporting materials
    key_terms: str = Field(..., description="Brief explanations of technical terms or concepts used in the story")
    impact_summary: str = Field(..., description="A summary of the long-term impact of this work on science or society")
    discussion_questions: List[str] = Field(..., description="Thought-provoking questions for readers to reflect on (3-5 questions)")
