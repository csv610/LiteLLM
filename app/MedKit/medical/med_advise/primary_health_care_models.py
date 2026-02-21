"""Pydantic models for primary health care response structure.

Defines the data models used for representing information provided by 
a primary health care provider to a patient.
"""

from pydantic import BaseModel, Field
from typing import Optional, List

from lite.config import ModelOutput


class PrimaryCareResponseModel(BaseModel):
    """
    Structured response from a primary health care provider.
    """
    understanding_concern: str = Field(description="A brief summary of the patient's concern or the topic")
    common_symptoms: List[str] = Field(description="List of common symptoms or observations related to the query")
    general_explanation: str = Field(description="Accessible explanation of the condition or health topic")
    self_care_advice: str = Field(description="General advice and practical self-care steps")
    when_to_seek_care: str = Field(description="Clear indicators for when to seek professional or urgent medical attention")
    next_steps: List[str] = Field(description="Recommended next steps or questions for a follow-up appointment")


    next_steps: List[str] = Field(description="Recommended next steps or questions for a follow-up appointment")
