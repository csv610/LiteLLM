"""
symptom_drugs_models.py - Data Models for Symptom-to-Drug Recommendations

This module contains all Pydantic models and Enums used for listing drugs
prescribed for specific symptoms, including drug types, rationale, and 
safety information.
"""

from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List


class DrugType(str, Enum):
    """
    Categorization of drug types.
    """
    GENERIC = "Generic"
    OTC = "OTC (Over-the-Counter)"
    RX = "Prescription (Rx)"
    HERBAL = "Herbal/Supplement"
    OTHER = "Other"


class DrugRecommendation(BaseModel):
    """Information about a specific drug recommended for a symptom."""
    drug_name: str = Field(description="Name of the drug (generic or brand)")
    drug_type: DrugType = Field(description="Type of the drug (Generic, OTC, Rx, etc.)")
    rationale: str = Field(description="Why this drug is typically prescribed for the symptom")
    common_dosage: Optional[str] = Field(
        default=None,
        description="Typical dosage or frequency for this symptom"
    )
    precautions: Optional[str] = Field(
        default=None,
        description="Important precautions or common side effects, comma-separated"
    )
    contraindications: Optional[str] = Field(
        default=None,
        description="Conditions or situations where this drug should be avoided, comma-separated"
    )


class SymptomDrugAnalysisModel(BaseModel):
    """Comprehensive analysis of drugs for a given symptom."""
    symptom_name: str = Field(description="Name of the symptom being analyzed")
    description: str = Field(description="Brief description of the symptom and its typical clinical context")
    recommended_drugs: List[DrugRecommendation] = Field(
        description="List of medically approved (e.g., FDA/EMA) drugs typically prescribed or recommended for this symptom. Do NOT include fabricated or unverified medicine names."
    )
    lifestyle_recommendations: Optional[str] = Field(
        default=None,
        description="Non-pharmacological or lifestyle recommendations for the symptom, comma-separated"
    )
    when_to_see_doctor: str = Field(
        description="Clear guidance on when this symptom requires urgent medical attention"
    )
    technical_summary: str = Field(
        description="Technical summary of pharmacological approach to this symptom"
    )


class ModelOutput(BaseModel):
    data: Optional[SymptomDrugAnalysisModel] = None
    markdown: Optional[str] = None
