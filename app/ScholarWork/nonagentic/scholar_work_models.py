"""
scholar_work_models.py - Pydantic models for scholar major works

Defines data models for generating and storing narrative-driven explanations
of major scientific work done by a given scientist.
"""

from pydantic import BaseModel, Field
from typing import List


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
