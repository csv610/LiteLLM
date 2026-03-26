"""
math_theory_models.py - Pydantic models for mathematical theory data

Defines data models for mathematical theories with explanations tailored to 
different audience levels (high-school, undergrad, master, phd, researcher).
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum


class AudienceLevel(str, Enum):
    GENERAL = "general"
    HIGH_SCHOOL = "high-school"
    UNDERGRAD = "undergrad"
    MASTER = "master"
    PHD = "phd"
    RESEARCHER = "researcher"


class SolutionMethods(BaseModel):
    """Analytical and numerical solution methods for the theory"""
    analytical: str = Field(..., description="Detailed analytical methods used to solve problems within this theory")
    numerical: str = Field(..., description="In-depth numerical or computational methods used for this theory")


class ResearchData(BaseModel):
    """Raw, detailed mathematical facts and context gathered by the Researcher agent"""
    theory_name: str
    detailed_history: str = Field(..., description="Comprehensive historical context and motivations")
    core_axioms_and_rules: List[str] = Field(..., description="The fundamental mathematical rules and axioms")
    key_theorems: List[str] = Field(..., description="Major theorems derived from this theory")
    modern_applications: List[str] = Field(..., description="Real-world and theoretical applications today")
    connected_theories: List[str] = Field(..., description="Theories that use this as a foundation")
    current_research_frontiers: str = Field(..., description="Open problems and active research areas")
    technical_solution_details: SolutionMethods


class TheoryExplanation(BaseModel):
    """Detailed explanation of a mathematical theory for a specific audience"""
    audience: AudienceLevel
    introduction: str = Field(..., description="A clear, lengthier introduction tailored to the audience")
    key_concepts: List[str] = Field(..., description="Fundamental concepts explained with appropriate complexity")
    why_it_was_created: str = Field(..., description="Historical context and motivation rewritten for the audience")
    problems_solved_or_simplified: str = Field(..., description="Specific problems explained at the right level")
    how_it_is_used_today: str = Field(..., description="Modern applications and usage of the theory")
    foundation_for_other_theories: str = Field(..., description="How this theory served as a basis for other developments")
    new_research: str = Field(..., description="Current areas of research and open questions")
    solution_methods: SolutionMethods = Field(..., description="Analytical and numerical solution methods")


class ReviewFeedback(BaseModel):
    """Feedback from the Reviewer agent regarding accuracy and audience appropriateness"""
    is_accurate: bool = Field(..., description="Whether the mathematical facts are correct")
    is_audience_appropriate: bool = Field(..., description="Whether the tone and complexity match the audience level")
    critique: str = Field(..., description="Specific points of improvement or praise")
    required_corrections: Optional[List[str]] = Field(default=None, description="List of specific mathematical or tonal corrections needed")


class MathTheory(BaseModel):
    """Comprehensive information about a mathematical theory across different audience levels"""
    theory_name: str = Field(..., description="The name of the mathematical theory")
    explanations: Dict[AudienceLevel, TheoryExplanation] = Field(..., description="Explanations tailored for each audience level")


class TheoryResponse(BaseModel):
    """Response wrapper for theory information"""
    theory: MathTheory
