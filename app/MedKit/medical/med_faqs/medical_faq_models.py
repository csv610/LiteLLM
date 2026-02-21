"""Pydantic models for medical FAQ generation.

This module defines the data structures for organizing patient-friendly and
provider-focused FAQ content with structured guidance on medical topics.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

from lite.config import ModelOutput


class FAQItem(BaseModel):
    """Single FAQ question-answer pair."""
    question: str = Field(description="The frequently asked question")
    answer: str = Field(description="Comprehensive answer to the question")


class MisconceptionItemModel(BaseModel):
    """Common misconception and clarification."""
    misconception: str = Field(description="The incorrect belief or myth")
    clarification: str = Field(description="The accurate medical information")
    explanation: str = Field(description="Why the misconception exists and how to address it")


class WhenToSeekCareModel(BaseModel):
    """Guidance on when patient should seek medical attention."""
    symptom_or_condition: str = Field(description="The symptom or condition indicator")
    urgency_level: str = Field(description="Urgency: immediate, urgent, soon, or routine")
    action_needed: str = Field(description="What action the patient should take")
    additional_context: Optional[str] = Field(default=None, description="Additional guidance")


class SeeAlsoTopicsModel(BaseModel):
    """Cross-reference to related medical topics, tests, or devices to explore."""
    name: str = Field(description="Name of the related topic, test, or device")
    category: str = Field(description="Category of reference: 'topic', 'test', or 'device'")
    description: str = Field(description="Brief description of what this reference covers")
    relevance: str = Field(description="Why this cross-reference is relevant to the current topic")


class PatientFAQModel(BaseModel):
    """Patient-friendly FAQ section."""
    topic_name: str = Field(description="Medical topic name")
    introduction: str = Field(description="Brief introduction to the topic")
    faqs: List[FAQItemModel] = Field(description="Patient-friendly Q&A pairs")
    when_to_seek_care: List[WhenToSeekCareModel] = Field(description="Guidance on when to seek medical attention")
    misconceptions: List[MisconceptionItemModel] = Field(description="Common myths and clarifications")
    see_also: List[SeeAlsoTopicsModel] = Field(description="Related topics, tests, and devices for further learning")


class ProviderFAQModel(BaseModel):
    """Provider-focused FAQ section with clinical depth."""
    topic_name: str = Field(description="Medical topic name")
    clinical_overview: str = Field(description="Clinical overview for healthcare providers")
    clinical_faqs: List[FAQItemModel] = Field(description="Clinically-focused Q&A pairs")
    evidence_based_practices: List[str] = Field(description="Current best practices and evidence")
    quality_metrics: List[str] = Field(description="Outcome measures and quality indicators")
    referral_criteria: List[str] = Field(description="When to refer to specialists")


class MedicalFAQModel(BaseModel):
    """Complete FAQ package with patient and optional provider sections."""
    topic_name: str = Field(description="Medical topic name")
    metadata: dict = Field(description="Metadata about generation")
    patient_faq: PatientFAQModel = Field(description="Patient-friendly FAQ section")
    provider_faq: Optional[ProviderFAQModel] = Field(default=None, description="Optional provider-focused FAQ section")

