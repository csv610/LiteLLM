"""
paradox_models.py - Pydantic models for paradox data

Defines data models for paradoxes with explanations tailored to 
different audience levels (general, high-school, undergrad, master, phd, researcher).
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum


class AudienceLevel(str, Enum):
    GENERAL = "general"
    HIGH_SCHOOL = "high-school"
    UNDERGRAD = "undergrad"
    MASTER = "master"
    PHD = "phd"
    RESEARCHER = "researcher"


class ParadoxStatus(str, Enum):
    SOLVED = "Solved"
    UNSOLVED = "Unsolved"
    DEBATED = "Under Debate"
    PARTIALLY_SOLVED = "Partially Solved"


class ParadoxResolution(BaseModel):
    """Logical and mathematical resolutions for the paradox"""
    who_solved: str = Field(..., description="The primary figures or schools of thought that solved or resolved the paradox")
    how_it_was_solved: str = Field(..., description="The specific breakthrough, method, or realization that led to the resolution")
    logical: str = Field(..., description="Logical or philosophical details of the resolution")
    mathematical: str = Field(..., description="Mathematical or scientific details of the resolution")


class ParadoxExplanation(BaseModel):
    """Detailed explanation of a paradox for a specific audience"""
    introduction: str = Field(..., description="A clear introduction to the paradox")
    status: ParadoxStatus = Field(..., description="Current status of the paradox (Solved, Unsolved, Under Debate, etc.)")
    root_cause: str = Field(..., description="The fundamental hidden assumptions in existing theories that lead to this paradox")
    key_concepts: List[str] = Field(..., description="A list of fundamental concepts necessary to understand this paradox")
    historical_context: str = Field(..., description="Historical context and motivation for the paradox")
    the_contradiction: str = Field(..., description="The core contradiction or counter-intuitive nature of the paradox")
    modern_relevance: str = Field(..., description="Modern applications and relevance of the paradox")
    impact_on_thought: str = Field(..., description="How this paradox influenced subsequent logical or scientific developments")
    current_debates: str = Field(..., description="Current areas of research and open questions related to this paradox")
    resolutions: ParadoxResolution = Field(..., description="Logical and mathematical resolutions including who and how")


class Paradox(BaseModel):
    """Comprehensive information about a paradox across different audience levels"""
    paradox_name: str = Field(..., description="The name of the paradox")
    explanations: Dict[AudienceLevel, ParadoxExplanation] = Field(..., description="Explanations tailored for each audience level")


class ParadoxResponse(BaseModel):
    """Response wrapper for paradox information"""
    paradox: Paradox
