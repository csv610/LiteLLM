from typing import Any

"""
deep_intuition_models.py - Models for the 5-Agent Deep Intuition Storytelling Engine
"""

from lite import ModelOutput


class HistoricalResearch(BaseModel):
    """Output from the Historical Researcher agent."""

    key_historical_anchors: List[str] = Field(
        ..., description="Specific historical events, people, or failures."
    )
    archive_of_failures_details: str = Field(
        ..., description="Detailed research notes on failed attempts."
    )


class IntuitionInsight(BaseModel):
    """Output from the Intuition Specialist agent."""

    the_aha_moment: str = Field(..., description="The moment of insight.")
    intuitive_analogy: str = Field(..., description="The core analogy.")
    core_insight_summary: str = Field(..., description="Summary of the core insight.")


class CounterfactualAnalysis(BaseModel):
    """Output from the Counterfactual Analyst agent."""

    counterfactual_world: str = Field(
        ..., description="A deep look at a world without this discovery."
    )
    modern_resonance: str = Field(
        ..., description="Current relevance and applications."
    )


class StruggleNarrative(BaseModel):
    """Output from the Human Struggle Narrator agent."""

    the_human_struggle: str = Field(..., description="The narrative of the struggle.")
    human_triumph_rationale: str = Field(
        ..., description="Why this was a persistence-based triumph."
    )


class DeepIntuitionStory(BaseModel):
    """The final synthesized story of a fundamental discovery."""

    topic: str = Field(..., description="The fundamental idea.")
    the_human_struggle: str = Field(
        ..., description="The story of the systematic exploration and failures."
    )
    the_aha_moment: str = Field(
        ..., description="The perspective shift explained through an analogy."
    )
    human_triumph_rationale: str = Field(
        ..., description="Why this was a triumph of persistence."
    )
    counterfactual_world: str = Field(
        ..., description="A look at a world without this discovery."
    )
    modern_resonance: str = Field(
        ..., description="Impact on our modern understanding."
    )
    key_historical_anchors: List[str] = Field(
        ..., description="Specific historical events or people."
    )
