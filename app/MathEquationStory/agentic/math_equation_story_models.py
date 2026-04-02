"""
math_equation_story_models.py - Pydantic models for mathematical equation stories

Defines data models for generating and storing narrative-driven explanations
of mathematical equations with supporting materials.
"""

from pydantic import BaseModel, Field
from typing import List


class ResearchBrief(BaseModel):
    """A detailed research brief about a mathematical equation."""
    equation_name: str = Field(..., description="The name of the equation")
    historical_context: str = Field(..., description="Who discovered it, when, and the problem they were solving")
    mathematical_core: str = Field(..., description="The fundamental mathematical principles and logic behind the equation")
    real_world_applications: List[str] = Field(..., description="3-5 concrete ways this equation is used today")
    key_metaphors: List[str] = Field(..., description="Potential analogies or metaphors to help explain the concept")
    common_misconceptions: List[str] = Field(..., description="Common ways people misunderstand this equation")

class MathematicalEquationStory(BaseModel):
    """A coherent narrative story explaining a mathematical equation"""
    equation_name: str = Field(..., description="Name of the equation being explained")
    latex_formula: str = Field(..., description="The LaTeX representation of the equation")
    title: str = Field(..., description="An engaging title for the story")
    subtitle: str = Field(..., description="A compelling subtitle or subheading")
    story: str = Field(..., description="The complete narrative story as flowing prose, written like a professional science article")
    vocabulary_notes: str = Field(..., description="Brief explanations of technical terms used in the story")
    discussion_questions: List[str] = Field(..., description="Thought-provoking questions for readers to reflect on (3-5 questions)")


MathEquationStory = MathematicalEquationStory


from typing import Any

class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
