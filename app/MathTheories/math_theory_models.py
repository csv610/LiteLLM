"""
math_theory_models.py - Pydantic models for mathematical theory data

Defines data models for mathematical theories with explanations tailored to 
different audience levels (high-school, undergrad, master, phd, researcher).
"""

from pydantic import BaseModel, Field
from typing import List, Dict
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
    analytical: str = Field(..., description="Analytical methods used to solve problems within this theory")
    numerical: str = Field(..., description="Numerical or computational methods used for this theory")


class TheoryExplanation(BaseModel):
    """Detailed explanation of a mathematical theory for a specific audience"""
    introduction: str = Field(..., description="A clear introduction to the theory")
    key_concepts: List[str] = Field(..., description="A list of fundamental concepts necessary to understand this theory")
    why_it_was_created: str = Field(..., description="Historical context and motivation for creating the theory")
    problems_solved_or_simplified: str = Field(..., description="Specific problems the theory solved or simplified")
    how_it_is_used_today: str = Field(..., description="Modern applications and usage of the theory")
    foundation_for_other_theories: str = Field(..., description="How this theory served as a basis for subsequent mathematical developments")
    new_research: str = Field(..., description="Current areas of research and open questions related to this theory")
    solution_methods: SolutionMethods = Field(..., description="Analytical and numerical solution methods")


class MathTheory(BaseModel):
    """Comprehensive information about a mathematical theory across different audience levels"""
    theory_name: str = Field(..., description="The name of the mathematical theory")
    explanations: Dict[AudienceLevel, TheoryExplanation] = Field(..., description="Explanations tailored for each audience level")


class TheoryResponse(BaseModel):
    """Response wrapper for theory information"""
    theory: MathTheory
