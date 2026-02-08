"""Pydantic models and enums for drug addiction analysis."""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class AddictionPotential(str, Enum):
    """Levels of addictive potential."""
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    VERY_HIGH = "Very High"
    EXTREME = "Extreme"


class WithdrawalSeverity(str, Enum):
    """Severity levels for withdrawal symptoms."""
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"
    LIFE_THREATENING = "Life-threatening"


class DEASchedule(str, Enum):
    """DEA Controlled Substance Schedules."""
    SCHEDULE_I = "Schedule I"
    SCHEDULE_II = "Schedule II"
    SCHEDULE_III = "Schedule III"
    SCHEDULE_IV = "Schedule IV"
    SCHEDULE_V = "Schedule V"
    NOT_SCHEDULED = "Not Scheduled"


class ConfidenceLevel(str, Enum):
    """Confidence levels in addiction assessment."""
    HIGH = "High"
    MODERATE = "Moderate"
    LOW = "Low"


class WithdrawalSymptomModel(BaseModel):
    """Information about a specific withdrawal symptom."""
    symptom: str = Field(description="Name of the withdrawal symptom")
    severity: WithdrawalSeverity = Field(description="Severity of this specific symptom")
    duration: Optional[str] = Field(default=None, description="Typical duration of the symptom")
    management: Optional[str] = Field(default=None, description="How to manage this symptom")


class AddictionMechanismModel(BaseModel):
    """Details on the biological and psychological mechanism of addiction."""
    neurotransmitter_impact: str = Field(description="Affected neurotransmitters (e.g., Dopamine, GABA)")
    psychological_factors: str = Field(description="Psychological drivers of addiction")
    physiological_dependence: str = Field(description="Nature of physical dependence")


class DrugAddictionDetailsModel(BaseModel):
    """Comprehensive drug addiction analysis."""
    medicine_name: str = Field(description="Name of the drug or medicine")
    other_names: Optional[List[str]] = Field(default=None, description="Alternative names, brand names, or street names")
    dea_schedule: Optional[DEASchedule] = Field(description="DEA Controlled Substance Schedule (e.g., Schedule I, II, etc.)")
    addiction_potential: AddictionPotential = Field(description="Overall potential for addiction")
    mechanism: AddictionMechanismModel = Field(description="Mechanisms of addiction")
    withdrawal_symptoms: List[WithdrawalSymptomModel] = Field(description="List of withdrawal symptoms")
    long_term_effects: List[str] = Field(description="Long-term physical and mental effects")
    risk_factors: List[str] = Field(description="Factors that increase the risk of addiction")
    treatment_options: List[str] = Field(description="Commonly used treatment and recovery options")
    prevention_strategies: List[str] = Field(description="Strategies to prevent addiction or dependence")
    confidence_level: ConfidenceLevel = Field(description="Confidence level in this assessment")
    references: Optional[str] = Field(default=None, description="Citations or references supporting this data")


class PatientFriendlyAddictionSummaryModel(BaseModel):
    """Patient-friendly explanation of drug addiction risks."""
    simple_explanation: str = Field(description="Simple explanation of addiction risk")
    signs_of_addiction: List[str] = Field(description="Warning signs for the patient or family")
    what_to_do: str = Field(description="Immediate steps if addiction is suspected")
    recovery_outlook: str = Field(description="General outlook for recovery and support")


class DrugAddictionModel(BaseModel):
    """
    Comprehensive drug addiction analysis result.

    Combines clinical data, mechanism details, and patient-friendly information
    to provide a full picture of addiction risk and management.
    """
    addiction_details: Optional[DrugAddictionDetailsModel] = Field(
        default=None,
        description="Detailed addiction information"
    )
    technical_summary: str = Field(
        description="Technical summary for healthcare professionals"
    )
    patient_friendly_summary: Optional[PatientFriendlyAddictionSummaryModel] = Field(
        default=None,
        description="Patient-friendly explanation"
    )


class ModelOutput(BaseModel):
    data: Optional[DrugAddictionModel] = None
    markdown: Optional[str] = None
