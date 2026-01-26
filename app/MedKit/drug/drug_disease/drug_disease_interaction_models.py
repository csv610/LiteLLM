"""
drug_disease_interaction_models.py - Data Models for Drug-Disease Interactions

This module contains all Pydantic models and Enums used for drug-disease
interaction analysis, including severity levels, confidence metrics, and
comprehensive interaction details.
"""

from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class InteractionSeverity(str, Enum):
    """
    Severity levels for drug-disease interactions.

    Severity scale from no interaction to absolute contraindication.

    Attributes:
        NONE: No clinically significant interaction
        MINOR: Minimal clinical significance, usually no action needed
        MILD: Small clinical effect, may need minor monitoring
        MODERATE: Notable clinical effect, usually requires intervention
        SIGNIFICANT: Major clinical concern, careful management required
        CONTRAINDICATED: Absolute contraindication, drug should not be used

    Example:
        severity = InteractionSeverity.MODERATE
        if severity in [InteractionSeverity.SIGNIFICANT, InteractionSeverity.CONTRAINDICATED]:
            print("High-risk interaction detected")
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

    Indicates the strength of evidence supporting the interaction claim.

    Attributes:
        HIGH: Strong evidence from multiple clinical studies and guidelines
        MODERATE: Adequate evidence from clinical studies or case reports
        LOW: Limited evidence, anecdotal reports, or theoretical basis

    Example:
        if interaction.confidence == ConfidenceLevel.LOW:
            print("Use caution - limited evidence for this interaction")
    """
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"


class DataSourceType(str, Enum):
    """
    Types of data sources for interaction information.

    Specifies where the interaction evidence originates.

    Attributes:
        CLINICAL_STUDIES: Data from peer-reviewed clinical trials
        PHARMACOKINETIC_ANALYSIS: Derived from drug metabolism studies
        FDA_WARNINGS: From FDA adverse event reports or black box warnings
        CASE_REPORTS: Individual case reports in medical literature
        CLINICAL_GUIDELINES: From professional clinical guidelines (AMA, ASAM, etc.)

    Example:
        source = DataSourceType.FDA_WARNINGS
    """
    CLINICAL_STUDIES = "Clinical Studies"
    PHARMACOKINETIC_ANALYSIS = "Pharmacokinetic Analysis"
    FDA_WARNINGS = "FDA Warnings"
    CASE_REPORTS = "Case Reports"
    CLINICAL_GUIDELINES = "Clinical Guidelines"


class ImpactType(str, Enum):
    """
    Type of impact the condition has on drug use.

    Categorizes how the disease/condition affects the drug therapy.

    Attributes:
        EFFICACY_REDUCTION: Drug becomes less effective
        EFFICACY_ENHANCEMENT: Drug becomes more effective (usually concerning)
        INCREASED_TOXICITY: Risk of adverse effects increases
        ALTERED_METABOLISM: Drug is processed differently by the body
        CONTRAINDICATED: Drug should not be used at all
        REQUIRES_MONITORING: Enhanced clinical monitoring needed
        REQUIRES_DOSE_ADJUSTMENT: Dose or frequency must be changed

    Example:
        impact = ImpactType.ALTERED_METABOLISM
    """
    EFFICACY_REDUCTION = "Reduced Drug Efficacy"
    EFFICACY_ENHANCEMENT = "Enhanced Drug Efficacy"
    INCREASED_TOXICITY = "Increased Toxicity Risk"
    ALTERED_METABOLISM = "Altered Drug Metabolism"
    CONTRAINDICATED = "Contraindicated"
    REQUIRES_MONITORING = "Requires Enhanced Monitoring"
    REQUIRES_DOSE_ADJUSTMENT = "Requires Dose Adjustment"


class EfficacyImpactModel(BaseModel):
    """Information about how the condition affects drug effectiveness."""
    has_impact: bool = Field(description="Whether the condition affects drug efficacy")
    impact_description: Optional[str] = Field(
        default=None,
        description="How the condition reduces, enhances, or otherwise affects drug effectiveness"
    )
    clinical_significance: Optional[str] = Field(
        default=None,
        description="The clinical importance of the efficacy impact"
    )
    monitoring_for_efficacy: Optional[str] = Field(
        default=None,
        description="How to monitor for adequate drug response, comma-separated"
    )


class SafetyImpactModel(BaseModel):
    """Information about how the condition affects drug safety."""
    has_impact: bool = Field(description="Whether the condition increases safety risks")
    impact_description: Optional[str] = Field(
        default=None,
        description="How the condition increases adverse effects or toxicity"
    )
    increased_side_effects: Optional[str] = Field(
        default=None,
        description="Specific side effects more likely to occur, comma-separated"
    )
    risk_level: Optional[InteractionSeverity] = Field(
        default=None,
        description="Risk severity (MINOR, MILD, MODERATE, SIGNIFICANT, CONTRAINDICATED)"
    )
    monitoring_for_safety: Optional[str] = Field(
        default=None,
        description="Safety monitoring parameters and labs to check, comma-separated"
    )


class DosageAdjustmentModel(BaseModel):
    """Dosage adjustment recommendations based on the condition."""
    adjustment_needed: bool = Field(description="Whether dose adjustment is necessary")
    adjustment_type: Optional[str] = Field(
        default=None,
        description="Type of adjustment (e.g., 'dose reduction', 'dose increase', 'dosing interval change')"
    )
    specific_recommendations: Optional[str] = Field(
        default=None,
        description="Specific dosage adjustment guidance and rationale"
    )
    monitoring_parameters: Optional[str] = Field(
        default=None,
        description="Labs or parameters to check when adjusting dose, comma-separated"
    )


class ManagementStrategyModel(BaseModel):
    """Overall management strategy for the drug-disease interaction."""
    impact_types: list[ImpactType] = Field(
        description="Types of impacts (efficacy, safety, metabolism, etc.)"
    )
    clinical_recommendations: str = Field(
        description="Comprehensive clinical recommendations for managing the interaction, comma-separated"
    )
    contraindication_status: Optional[str] = Field(
        default=None,
        description="Whether drug is contraindicated, relatively contraindicated, or safe with precautions"
    )
    alternative_treatments: Optional[str] = Field(
        default=None,
        description="Alternative medications or approaches for patients with this condition, comma-separated"
    )


class DrugDiseaseInteractionDetailsModel(BaseModel):
    """Comprehensive drug-disease interaction analysis."""
    medicine_name: str = Field(description="Name of the medicine")
    condition_name: str = Field(description="Name of the medical condition")
    overall_severity: InteractionSeverity = Field(
        description="Overall severity of the interaction"
    )
    mechanism_of_interaction: str = Field(
        description="How the condition affects the drug's action, metabolism, or efficacy at the molecular/physiological level"
    )
    efficacy_impact: EfficacyImpactModel = Field(
        description="How the condition affects drug effectiveness"
    )
    safety_impact: SafetyImpactModel = Field(
        description="How the condition affects drug safety"
    )
    dosage_adjustment: DosageAdjustmentModel = Field(
        description="Dosage adjustment recommendations if needed"
    )
    management_strategy: ManagementStrategyModel = Field(
        description="Overall management strategy and clinical approach"
    )
    confidence_level: ConfidenceLevel = Field(
        description="Confidence level in this interaction assessment"
    )
    data_source_type: DataSourceType = Field(
        description="Primary source of this interaction data"
    )
    references: Optional[str] = Field(
        default=None,
        description="Citations or references supporting this interaction data, comma-separated"
    )


class PatientFriendlySummaryModel(BaseModel):
    """Patient-friendly explanation of drug-disease interactions."""
    simple_explanation: str = Field(
        description="Simple explanation of how the condition affects this medicine"
    )
    what_patient_should_do: str = Field(
        description="Clear action steps for managing the condition-medicine interaction"
    )
    signs_of_problems: str = Field(
        description="Symptoms or signs that indicate the medicine may not be working properly or causing problems, comma-separated"
    )
    when_to_contact_doctor: str = Field(
        description="Clear guidance on when to contact healthcare provider"
    )
    lifestyle_modifications: str = Field(
        description="Lifestyle changes that may help manage the interaction, comma-separated"
    )


class DataAvailabilityModel(BaseModel):
    """Information about data availability."""
    data_available: bool = Field(
        description="Whether interaction data is available"
    )
    reason: Optional[str] = Field(
        default=None,
        description="Explanation if data is not available"
    )


class DrugDiseaseInteractionModel(BaseModel):
    """
    Comprehensive drug-disease interaction analysis result.

    Combines clinical data, patient education, and management strategies
    in a structured format for healthcare professionals and patients.
    """

    interaction_details: Optional[DrugDiseaseInteractionDetailsModel] = Field(
        default=None,
        description="Detailed interaction information (None if data not available)"
    )
    technical_summary: str = Field(
        description="Technical summary suitable for healthcare professionals"
    )
    patient_friendly_summary: Optional[PatientFriendlySummaryModel] = Field(
        default=None,
        description="Patient-friendly explanation"
    )
    data_availability: DataAvailabilityModel = Field(
        description="Status of data availability"
    )


class ModelOutput(BaseModel):
    data: Optional[DrugDiseaseInteractionModel] = None
    markdown: Optional[str] = None

