"""
faq_generator_models.py - Pydantic models for FAQ generation

Defines data models for representing frequently asked questions and responses
with comprehensive validation and structured data organization.
"""

from pydantic import BaseModel, Field
from typing import List, Literal

# Centralized list of valid difficulty levels
VALID_DIFFICULTIES = ["simple", "medium", "hard", "research"]
DifficultyLevel = Literal["simple", "medium", "hard", "research"]

class FAQ(BaseModel):
    """Represents a single FAQ entry."""
    question: str = Field(..., description="The frequently asked question")
    answer: str = Field(..., description="The answer to the question")
    difficulty: DifficultyLevel = Field(..., description="Difficulty level (simple, medium, hard, research)")


class FAQResponse(BaseModel):
    """Response containing a list of FAQs."""
    topic: str = Field(..., description="The topic for which FAQs are provided")
    difficulty: DifficultyLevel = Field(..., description="Difficulty level (simple, medium, hard, research)")
    num_faqs: int = Field(..., description="Number of FAQs generated")
    faqs: List[FAQ]
