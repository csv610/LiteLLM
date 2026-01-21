"""Pydantic models for drugs comparison module.

Defines all data structures for medicines comparison including clinical metrics,
regulatory information, practical details, and comprehensive comparison results.
"""

from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class EffectivenessRating(str, Enum):
    """Effectiveness ratings for a medicine."""
    VERY_LOW = "Very Low"
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    VERY_HIGH = "Very High"


class SafetyRating(str, Enum):
    """Safety ratings for a medicine."""
    VERY_HIGH_RISK = "Very High Risk"
    HIGH_RISK = "High Risk"
    MODERATE_RISK = "Moderate Risk"
    LOW_RISK = "Low Risk"
    VERY_LOW_RISK = "Very Low Risk"


class AvailabilityStatus(str, Enum):
    """Availability status of a medicine."""
    PRESCRIPTION_ONLY = "Prescription Only (Rx)"
    OVER_THE_COUNTER = "Over-the-Counter (OTC)"
    CONTROLLED_SUBSTANCE = "Controlled Substance"
    RESTRICTED_DISTRIBUTION = "Restricted Distribution"
    DISCONTINUED = "Discontinued"


class ClinicalMetrics(BaseModel):
    """Clinical effectiveness and safety metrics for a medicine."""
    medicine_name: str = Field(description="Name of the medicine")
    effectiveness_rating: EffectivenessRating = Field(description="Overall effectiveness rating")
    efficacy_rate: str = Field(description="Clinical efficacy percentage or success rate from studies")
    onset_of_action: str = Field(description="How quickly the medicine starts working")
    duration_of_effect: str = Field(description="How long the effects typically last")
    safety_rating: SafetyRating = Field(description="Overall safety rating")
    common_side_effects: str = Field(description="Most commonly reported side effects, comma-separated")
    serious_side_effects: str = Field(description="Rare but serious adverse effects, comma-separated")
    black_box_warning: Optional[str] = Field(
        default=None,
        description="FDA black box warning if applicable"
    )
    contraindications: str = Field(description="Key contraindications, comma-separated")


class RegulatoryMetrics(BaseModel):
    """Regulatory and approval information for a medicine."""
    medicine_name: str = Field(description="Name of the medicine")
    fda_approval_status: str = Field(description="FDA approval status and indication")
    approval_date: str = Field(description="Date FDA approved the medicine")
    approval_type: str = Field(description="Approval type (e.g., Standard, Accelerated, Breakthrough, Priority)")
    has_black_box_warning: bool = Field(description="Whether medicine has FDA black box warning")
    fda_alerts: str = Field(description="Current FDA alerts or safety warnings, comma-separated")
    generic_available: bool = Field(description="Whether generic version is available")
    generic_date: Optional[str] = Field(
        default=None,
        description="When generic became available (if applicable)"
    )
    patent_expiration: Optional[str] = Field(
        default=None,
        description="Patent expiration date if still under patent"
    )


class PracticalMetrics(BaseModel):
    """Cost, availability, and practical information for a medicine."""
    medicine_name: str = Field(description="Name of the medicine")
    availability_status: AvailabilityStatus = Field(description="Prescription, OTC, controlled, etc.")
    typical_cost_range: str = Field(description="Typical cost range without insurance")
    insurance_coverage: str = Field(description="How typically covered by major insurance")
    available_formulations: str = Field(description="Available pharmaceutical forms, comma-separated")
    dosage_strengths: str = Field(description="Available dosage strengths, comma-separated")
    generic_cost: Optional[str] = Field(
        default=None,
        description="Typical cost of generic version if available"
    )
    patient_assistance_programs: str = Field(
        description="Available manufacturer assistance programs, comma-separated"
    )


class ComparisonSummary(BaseModel):
    """Summary of key differences between two medicines."""
    more_effective: str = Field(description="Which medicine is more effective and why")
    safer_option: str = Field(description="Which medicine has better safety profile and why")
    more_affordable: str = Field(description="Which medicine is more affordable and cost analysis")
    easier_access: str = Field(description="Which medicine is easier to access/obtain")
    key_differences: str = Field(
        description="Top 3-5 key differences between the medicines, comma-separated"
    )


class RecommendationContext(BaseModel):
    """Contextual recommendations for medicine selection."""
    for_acute_conditions: Optional[str] = Field(
        default=None,
        description="Which medicine is better for acute/short-term use and why"
    )
    for_chronic_conditions: Optional[str] = Field(
        default=None,
        description="Which medicine is better for chronic/long-term use and why"
    )
    for_elderly_patients: Optional[str] = Field(
        default=None,
        description="Which medicine is better for elderly patients and why"
    )
    for_cost_sensitive: Optional[str] = Field(
        default=None,
        description="Which medicine is better for cost-sensitive patients and why"
    )
    overall_recommendation: str = Field(
        description="Overall recommendation summary for typical patients"
    )


class MedicinesComparisonResult(BaseModel):
    """
    Comprehensive side-by-side comparison of two medicines.

    Includes clinical, regulatory, and practical metrics with detailed
    narrative analysis and contextual recommendations.
    """
    medicine1_clinical: ClinicalMetrics = Field(description="Clinical metrics for first medicine")
    medicine2_clinical: ClinicalMetrics = Field(description="Clinical metrics for second medicine")

    medicine1_regulatory: RegulatoryMetrics = Field(description="Regulatory metrics for first medicine")
    medicine2_regulatory: RegulatoryMetrics = Field(description="Regulatory metrics for second medicine")

    medicine1_practical: PracticalMetrics = Field(description="Practical metrics for first medicine")
    medicine2_practical: PracticalMetrics = Field(description="Practical metrics for second medicine")

    comparison_summary: ComparisonSummary = Field(description="Summary of key differences")
    recommendations: RecommendationContext = Field(description="Contextual recommendations")

    narrative_analysis: str = Field(
        description="Detailed narrative comparison analyzing similarities and differences"
    )

    evidence_quality: str = Field(
        description="Quality of evidence supporting comparison (high, moderate, low)"
    )

    limitations: str = Field(
        description="Limitations of this comparison and factors to consider, comma-separated"
    )
