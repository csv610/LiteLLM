"""
deep_intuition_models.py - Models for the Deep Intuition Storytelling Engine

Defines the structured narrative of a fundamental human discovery.
"""

from pydantic import BaseModel, Field
from typing import List


class DeepIntuitionStory(BaseModel):
    """The complete story of a fundamental discovery as a human triumph."""
    topic: str = Field(..., description="The fundamental idea (e.g., 'Gödel's Theorem').")
    
    the_human_struggle: str = Field(
        ..., 
        description="The story of the systematic exploration, the failed attempts, and the intellectual dead ends that preceded the discovery."
    )
    
    the_aha_moment: str = Field(
        ..., 
        description="The specific perspective shift or 'click' that made the discovery possible. Explained through an intuitive analogy."
    )
    
    human_triumph_rationale: str = Field(
        ..., 
        description="Why this was a triumph of persistence and systematic work, rather than 'magic' or superhuman intelligence."
    )
    
    counterfactual_world: str = Field(
        ..., 
        description="A deep look at how our world, technology, or mathematics would be stalled or different if this discovery was never made."
    )
    
    modern_resonance: str = Field(
        ..., 
        description="How this discovery impacts our modern understanding and why it still matters today."
    )
    
    key_historical_anchors: List[str] = Field(
        ..., 
        description="Specific historical events, people, or earlier 'failures' that anchor this story in reality."
    )
