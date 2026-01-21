"""
drug_drug_interaction_models.py - Pydantic data models for drug-drug interaction analysis

Defines the structured data models for drug interaction analysis, including
interaction details, patient summaries, and result aggregation.
"""

from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class DrugInteractionSeverity(str, Enum):
    """
    Severity levels for drug-drug interactions.

    Indicates how serious the interaction is and what clinical action is needed.

    Attributes:
        NONE: No clinically significant interaction
        MINOR: Minimal clinical significance, usually no action needed
        MILD: Small clinical effect, may need minor monitoring
        MODERATE: Notable clinical effect, usually requires intervention
        SIGNIFICANT: Major clinical concern, careful management required
        CONTRAINDICATED: Absolute contraindication, drugs should not be combined

    Example:
        severity = DrugInteractionSeverity.SIGNIFICANT
    """
    NONE = "NONE"
    MINOR = "MINOR"
    MILD = "MILD"
    MODERATE = "MODERATE"
    SIGNIFICANT = "SIGNIFICANT"
    CONTRAINDICATED = "CONTRAINDICATED"


class ConfidenceLevel(str, Enum):
    """
    Confidence levels in interaction assessment.

    Indicates strength of evidence supporting the interaction claim.

    Attributes:
        HIGH: Strong evidence from clinical studies and guidelines
        MODERATE: Adequate evidence from research or case reports
        LOW: Limited evidence, theoretical basis, or anecdotal reports

    Example:
        confidence = ConfidenceLevel.HIGH
    """
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"


class DataSourceType(str, Enum):
    """
    Types of data sources for interaction information.

    Specifies where the interaction evidence originates.

    Attributes:
        CLINICAL_STUDIES: Peer-reviewed clinical trial data
        PHARMACOKINETIC_ANALYSIS: Derived from drug metabolism studies
        AI_GENERATED: Generated using AI analysis
        CASE_REPORTS: Individual case reports in medical literature
        REGULATORY_DATA: FDA or other regulatory agency data

    Example:
        source = DataSourceType.CLINICAL_STUDIES
    """
    CLINICAL_STUDIES = "Clinical Studies"
    PHARMACOKINETIC_ANALYSIS = "Pharmacokinetic Analysis"
    AI_GENERATED = "AI-Generated"
    CASE_REPORTS = "Case Reports"
    REGULATORY_DATA = "Regulatory Data"


class DrugInteractionDetails(BaseModel):
    """
    Detailed information about a drug-drug interaction.

    Includes comprehensive analysis of how two drugs interact, clinical effects,
    and management recommendations for healthcare providers.

    Attributes:
        drug1_name (str): Name of the first medicine
        drug2_name (str): Name of the second medicine
        severity_level (DrugInteractionSeverity): How serious the interaction is
        mechanism_of_interaction (str): How drugs interact chemically/pharmacologically
        clinical_effects (str): Observable clinical effects and symptoms
        management_recommendations (str): How to handle the interaction

    Example:
        interaction = DrugInteractionDetails(
            drug1_name="Warfarin",
            drug2_name="Aspirin",
            severity_level=DrugInteractionSeverity.SIGNIFICANT,
            mechanism_of_interaction="Both drugs inhibit hemostasis...",
            clinical_effects="Increased bleeding risk",
            management_recommendations="Monitor INR, avoid if possible"
        )
    """
    drug1_name: str = Field(description="Name of the first medicine")
    drug2_name: str = Field(description="Name of the second medicine")
    severity_level: DrugInteractionSeverity = Field(
        description="Severity of the interaction (NONE, MINOR, MILD, MODERATE, SIGNIFICANT, CONTRAINDICATED)"
    )
    mechanism_of_interaction: str = Field(
        description="Detailed explanation of how the two drugs interact at the molecular/cellular level"
    )
    clinical_effects: str = Field(
        description="Observable clinical effects and symptoms of the interaction, comma-separated"
    )
    management_recommendations: str = Field(
        description="Clinical recommendations for managing the interaction (dose adjustments, monitoring, spacing, etc.), comma-separated"
    )
    alternative_medicines: str = Field(
        description="Alternative medicines that could be substituted for safer combinations, comma-separated"
    )
    confidence_level: ConfidenceLevel = Field(
        description="Confidence level in this interaction assessment (HIGH, MODERATE, LOW)"
    )
    data_source_type: DataSourceType = Field(
        description="Primary source of this interaction data"
    )
    references: Optional[str] = Field(
        default=None,
        description="Citations or references supporting this interaction data, comma-separated"
    )


class PatientFriendlySummary(BaseModel):
    """Patient-friendly explanation of the interaction."""
    simple_explanation: str = Field(
        description="Simple, non-technical explanation of what happens when these medicines interact"
    )
    what_patient_should_do: str = Field(
        description="Clear action steps for the patient (e.g., inform doctor, take at different times, etc.)"
    )
    warning_signs: str = Field(
        description="Symptoms or signs the patient should watch for, comma-separated"
    )
    when_to_seek_help: str = Field(
        description="Clear guidance on when to seek immediate medical attention"
    )


class DataAvailabilityInfo(BaseModel):
    """Information about data availability."""
    data_available: bool = Field(
        description="Whether interaction data is available"
    )
    reason: Optional[str] = Field(
        default=None,
        description="Explanation if data is not available (e.g., 'No interactions found in database', 'Limited research available', etc.)"
    )


class DrugInteractionResult(BaseModel):
    """
    Comprehensive drug-drug interaction analysis result.

    Combines clinical data, patient education, and availability information
    in a structured format for healthcare professionals and patients.
    """
    interaction_details: Optional[DrugInteractionDetails] = Field(
        default=None,
        description="Detailed interaction information (None if no interaction or data not available)"
    )
    technical_summary: str = Field(
        description="Technical summary of the interaction suitable for healthcare professionals"
    )
    patient_friendly_summary: Optional[PatientFriendlySummary] = Field(
        default=None,
        description="Patient-friendly explanation (None if no interaction)"
    )
    data_availability: DataAvailabilityInfo = Field(
        description="Status of data availability for this interaction check"
    )
