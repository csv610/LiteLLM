"""Pydantic models for primary health care response structure."""

from typing import List, Optional

from pydantic import BaseModel, Field


class TriageResponseModel(BaseModel):
    """Structured response from the Triage Agent."""
    understanding_concern: str = Field(
        description="A brief summary of the patient's concern or the topic"
    )
    common_symptoms: List[str] = Field(
        description="List of common symptoms or observations related to the query"
    )


class EducationResponseModel(BaseModel):
    """Structured response from the Medical Educator Agent."""
    general_explanation: str = Field(
        description="Accessible explanation of the condition or health topic"
    )


class SelfCareResponseModel(BaseModel):
    """Structured response from the Self-Care Advisor Agent."""
    self_care_advice: str = Field(
        description="General advice and practical self-care steps"
    )


class ClinicalResponseModel(BaseModel):
    """Structured response from the Clinical Guidance Agent."""
    when_to_seek_care: str = Field(
        description="Clear indicators for when to seek professional or urgent medical attention"
    )
    next_steps: List[str] = Field(
        description="Recommended next steps or questions for a follow-up appointment"
    )


class PrimaryCareResponseModel(BaseModel):
    """
    Structured response from a primary health care provider (Synthesized).
    """

    understanding_concern: str = Field(
        description="A brief summary of the patient's concern or the topic"
    )
    common_symptoms: List[str] = Field(
        description="List of common symptoms or observations related to the query"
    )
    general_explanation: str = Field(
        description="Accessible explanation of the condition or health topic"
    )
    self_care_advice: str = Field(
        description="General advice and practical self-care steps"
    )
    when_to_seek_care: str = Field(
        description="Clear indicators for when to seek professional or urgent medical attention"
    )
    next_steps: List[str] = Field(
        description="Recommended next steps or questions for a follow-up appointment"
    )


class ModelOutput(BaseModel):
    data: Optional[PrimaryCareResponseModel] = None
    markdown: Optional[str] = None
