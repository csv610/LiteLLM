"""
mathematical_equation_story_models.py - Pydantic models for mathematical equation stories

Defines data models for generating and storing narrative-driven explanations
of mathematical equations with supporting materials.
"""

from pydantic import BaseModel, Field
from typing import List


class MathematicalEquationStory(BaseModel):
    """A coherent narrative story explaining a mathematical equation"""
    equation_name: str = Field(..., description="Name of the equation being explained")
    latex_formula: str = Field(..., description="The LaTeX representation of the equation")
    title: str = Field(..., description="An engaging title for the story")
    subtitle: str = Field(..., description="A compelling subtitle or subheading")

    # The complete narrative - a flowing story, not fragmented sections
    story: str = Field(..., description="The complete narrative story as flowing prose, written like a professional science article")

    # Supporting materials
    vocabulary_notes: str = Field(..., description="Brief explanations of technical terms used in the story")
    discussion_questions: List[str] = Field(..., description="Thought-provoking questions for readers to reflect on (3-5 questions)")
