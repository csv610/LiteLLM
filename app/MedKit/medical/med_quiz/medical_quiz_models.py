"""Pydantic models for medical quiz generation.

This module defines the data structures for organizing board-style 
medical quiz questions, options, and explanations.
"""

from typing import List, Optional, Union, Dict
from pydantic import BaseModel, Field


class QuizQuestionModel(BaseModel):
    """A single multiple-choice question."""
    id: int = Field(ge=1, description="Question number (must be >= 1)")
    question: str = Field(min_length=10, description="The quiz question text")
    options: Dict[str, str] = Field(description="Dictionary of options (e.g., {'A': 'option text', 'B': 'option text'})")
    answer: str = Field(regex=r'^[A-Z]$', description="The correct answer key (e.g., 'A', 'B', 'C', 'D')")
    explanation: str = Field(min_length=20, description="Explanation of why the answer is correct")


class MedicalQuizModel(BaseModel):
    """Complete medical quiz package."""
    topic: str = Field(description="The main topic of the quiz")
    difficulty: str = Field(description="Overall difficulty level")
    questions: List[QuizQuestionModel] = Field(description="List of quiz questions")


class ModelOutput(BaseModel):
    data: Optional[MedicalQuizModel] = None
    markdown: Optional[str] = None
