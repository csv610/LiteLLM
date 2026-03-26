"""
Pydantic models for Riemann Theory Reference Guide.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class RiemannTheoryModel(BaseModel):
    """Structured data for a Riemann-related theory or concept."""
    name: str = Field(description="Name of the Riemann theory or concept")
    definition: str = Field(description="Formal mathematical or conceptual definition")
    layperson_explanation: str = Field(description="A simple, non-mathematical explanation of the core idea for a layperson")
    intuition: str = Field(description="The 'bigger picture' and intuitive explanation of the theory")
    motivation: str = Field(description="The specific problems Riemann was trying to solve and why the theory was created")
    misconceptions: List[str] = Field(description="Common misconceptions or myths about this theory and the reality behind them")
    historical_context: str = Field(description="History and origin of the theory")
    limitations: str = Field(description="The boundaries of the theory and what it does not solve")
    modern_developments: str = Field(description="How the theory has been refined, generalized, or progressed in modern mathematics")
    counterfactual_impact: str = Field(description="How modern science and mathematics would be different if this core idea were not developed")
    key_properties: List[str] = Field(description="Key properties or characteristics")
    applications: List[str] = Field(description="Applications in mathematics, physics, or other fields")
    related_concepts: List[str] = Field(description="Related Riemann or mathematical concepts")
    significance: str = Field(description="Significance of this theory in modern science")
