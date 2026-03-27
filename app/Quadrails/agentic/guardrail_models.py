"""
Pydantic models for text and image guardrailing.
"""

from typing import List
from pydantic import BaseModel, Field
from enum import Enum


class GuardrailError(Exception):
    """Base exception for all guardrail-related errors."""
    pass


class PreprocessingError(GuardrailError):
    """Raised when text cleaning or truncation fails."""
    pass


class AnalysisError(GuardrailError):
    """Raised when the LLM analysis fails to produce a valid response."""
    pass


class SafetyCategory(str, Enum):
    """Safety categories for guardrailing."""
    HATE_SPEECH = "hate_speech"
    ABUSIVE = "abusive"
    ILLEGAL = "illegal"
    HARASSMENT = "harassment"
    SELF_HARM = "self_harm"
    SEXUAL_CONTENT = "sexual_content"
    VIOLENT_CONTENT = "violent_content"
    PROFANITY = "profanity"
    PII = "pii"
    SPECIALIZED_ADVICE = "specialized_advice"
    JAILBREAK = "jailbreak"
    DEFAMATION = "defamation"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    ELECTIONS = "elections"
    INDISCRIMINATE_WEAPONS = "indiscriminate_weapons"
    NUDITY = "nudity"
    VIOLENCE = "violence"


class GuardrailResult(BaseModel):
    """Result of a guardrail check for a specific category."""
    category: SafetyCategory = Field(description="The safety category being checked")
    is_flagged: bool = Field(description="Whether the content violates this category")
    score: float = Field(description="Confidence score for the violation (0.0 to 1.0)")
    reasoning: str = Field(description="Brief explanation for the flagging decision")


class GuardrailResponse(BaseModel):
    """Structured response for content guardrailing."""
    text: str = Field(description="The input text that was analyzed")
    is_safe: bool = Field(description="Overall safety assessment (true if no categories are flagged)")
    flagged_categories: List[GuardrailResult] = Field(description="List of flagged safety categories")
    summary: str = Field(description="A concise summary of the safety assessment")


class ImageGuardrailResponse(BaseModel):
    """Structured response for image guardrailing."""
    image_path: str = Field(description="The path to the image that was analyzed")
    is_safe: bool = Field(description="Overall safety assessment (true if no categories are flagged)")
    flagged_categories: List[GuardrailResult] = Field(description="List of flagged safety categories")
    summary: str = Field(description="A concise summary of the safety assessment")
