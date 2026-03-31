"""
deep_deliberation_models.py - Models for the Knowledge Discovery Engine

Defines structured data for adversarial analysis and insight synthesis.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class DiscoveryFAQ(BaseModel):
    """A strategic question designed to uncover hidden knowledge or gaps."""
    question: str = Field(..., description="The targeted question to probe a specific knowledge gap.")
    rationale: str = Field(..., description="The strategic reason why this question will lead to a non-obvious discovery.")


class InitialKnowledgeMap(BaseModel):
    """The starting point for a knowledge discovery mission."""
    topic: str = Field(..., description="The main field of inquiry.")
    core_pillars: List[str] = Field(..., description="The established facts or pillars of the topic.")
    discovery_faqs: List[DiscoveryFAQ] = Field(..., description="Initial strategic questions to probe the unknown.")


class DiscoveryInsight(BaseModel):
    """A detailed analytical response designed to uncover new information."""
    analysis: str = Field(..., description="Deep dive analysis of the current sub-topic.")
    evidence: List[str] = Field(..., description="Key pieces of evidence or citations supporting the analysis.")
    counter_arguments: Optional[str] = Field(None, description="Potential flaws, contradictions, or opposing views.")
    new_discovery_faq: DiscoveryFAQ = Field(..., description="A new strategic question born from this analysis.")


class DiscoveryCheck(BaseModel):
    """The adversarial gatekeeper ensuring the discovery adds real value."""
    is_novel: bool = Field(..., description="True if the insight provides a non-obvious connection or identifies a genuine gap.")
    discovery_score: int = Field(..., description="A score from 1-10 on the density of new knowledge discovered.")
    reasoning: str = Field(..., description="Critique of the insight's novelty and depth.")


class VerificationResult(BaseModel):
    """Adversarial verification of the evidence provided."""
    is_verified: bool = Field(..., description="True if the evidence and logic are sound and non-hallucinated.")
    flaws_identified: Optional[List[str]] = Field(None, description="Specific flaws, hallucinations, or logical leaps found.")
    credibility_score: int = Field(..., description="A score from 1-10 on the reliability of the evidence.")
    critique: str = Field(..., description="Detailed adversarial critique of the evidence and analysis.")


class SummaryResponse(BaseModel):
    """A dense summary of the discovery for the next query's context."""
    summary: str = Field(..., description="A 2-3 sentence summary of the key insight and its evidence.")


class KnowledgeSynthesis(BaseModel):
    """The final map of discovered knowledge, connections, and frontiers."""
    topic: str = Field(..., description="The main field of inquiry.")
    executive_summary: str = Field(..., description="A high-level synthesis of the discovery mission.")
    hidden_connections: List[str] = Field(..., description="Non-obvious links identified between sub-topics.")
    research_frontiers: List[str] = Field(..., description="The 'Bleeding Edge'—where current knowledge ends and inquiry begins.")
