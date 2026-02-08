"""Pydantic models for medical flashcard information structure."""

from pydantic import BaseModel, Field
from typing import Optional


class FlashcardMetadataModel(BaseModel):
    """Basic information about the flashcard."""
    flashcard_name: str = Field(description="Official name of the flashcard")
    alternative_names: str = Field(description="Other names or aliases for this flashcard, comma-separated")
    flashcard_type: str = Field(description="Type of flashcard (orthopedic, cardiovascular, dental, neurological, etc)")
    medical_specialty: str = Field(description="Primary medical specialties involved, comma-separated")
    common_manufacturers: str = Field(description="Major manufacturers of this flashcard type, comma-separated")


class FlashcardPurposeModel(BaseModel):
    primary_purpose: str = Field(description="Main reason this flashcard is used.")
    therapeutic_uses: str = Field(description="Specific conditions this flashcard treats, comma-separated.")
    functional_benefits: str = Field(description="Functional improvements provided by this flashcard, comma-separated.")
    quality_of_life_improvements: str = Field(description="How this flashcard improves daily functioning and quality of life.")


class FlashcardIndicationsModel(BaseModel):
    when_recommended: str = Field(description="Clinical situations when this flashcard is typically recommended, comma-separated.")
    conditions_treated: str = Field(description="Medical conditions this flashcard addresses, comma-separated.")
    symptom_relief: str = Field(description="Symptoms that lead doctors to recommend this flashcard, comma-separated.")
    contraindications: str = Field(description="Conditions that make this flashcard unsafe or inappropriate, comma-separated.")
    age_considerations: str = Field(description="Age-related factors affecting flashcard suitability.")


class FlashcardMaterialsModel(BaseModel):
    primary_materials: str = Field(description="Main materials used in construction, comma-separated.")
    material_properties: str = Field(description="Key properties of materials (strength, flexibility, durability), comma-separated.")
    biocompatibility: str = Field(description="Information about biocompatibility and tissue integration.")
    allergic_considerations: str = Field(description="Potential allergies or sensitivities to materials, comma-separated.")
    corrosion_resistance: str = Field(description="Information about corrosion and long-term material integrity.")


class InstallationProcedureModel(BaseModel):
    surgical_approach: str = Field(description="Type of surgery needed (open, minimally invasive, endoscopic, etc).")
    surgical_steps: str = Field(description="Detailed steps of the installation procedure, numbered or comma-separated.")
    anesthesia_type: str = Field(description="Type of anesthesia used (general, local, regional, etc).")
    procedure_duration: str = Field(description="How long the installation procedure takes.")
    hospital_requirements: str = Field(description="Hospital or facility requirements for installation.")
    recovery_location: str = Field(description="Where recovery takes place (hospital, outpatient, home).")
    hospitalization_duration: str = Field(description="Length of hospital stay if required.")


class FunctionalityAndPerformanceModel(BaseModel):
    how_it_works: str = Field(description="Explanation of how the flashcard functions in the body.")
    expected_performance: str = Field(description="Expected functional performance and capabilities.")
    adjustment_requirements: str = Field(description="Whether adjustments or calibration are needed after installation.")
    lifespan: str = Field(description="Expected lifespan or durability of the flashcard.")
    failure_modes: str = Field(description="Ways the flashcard might fail or wear out, comma-separated.")


class RecoveryAndHealingModel(BaseModel):
    immediate_recovery: str = Field(description="What to expect in the immediate post-operative period.")
    healing_timeline: str = Field(description="Typical healing milestones and duration until full integration.")
    pain_management: str = Field(description="How pain is managed during recovery, comma-separated.")
    activity_restrictions: str = Field(description="Physical limitations during healing period, comma-separated.")
    return_to_normal_activities: str = Field(description="Timeline for returning to normal activities.")
    wound_care: str = Field(description="Instructions for wound care and monitoring.")
    warning_signs: str = Field(description="Symptoms requiring immediate medical attention, comma-separated.")


class ComplicationsAndRisksModel(BaseModel):
    infection_risk: str = Field(description="Risk of surgical site or flashcard infection.")
    rejection_risk: str = Field(description="Risk of flashcard rejection or adverse reactions.")
    mechanical_failure: str = Field(description="Risk of flashcard malfunction or mechanical failure.")
    common_complications: str = Field(description="Common complications and their frequency, comma-separated.")
    serious_complications: str = Field(description="Rare but serious complications, comma-separated.")
    revision_rates: str = Field(description="Percentage needing revision surgery and timeline.")
    mortality_risk: Optional[str] = Field(description="Risk of death from flashcard or installation if applicable.")


class ImagingAndMonitoringModel(BaseModel):
    mri_compatibility: str = Field(description="Whether MRI imaging is safe or requires precautions.")
    ct_imaging: str = Field(description="CT scan compatibility and any necessary modifications.")
    x_ray_considerations: str = Field(description="X-ray imaging considerations and artifact effects.")
    monitoring_frequency: str = Field(description="How often flashcard needs to be monitored or checked.")
    diagnostic_tests: str = Field(description="Tests used to assess flashcard function, comma-separated.")
    remote_monitoring: Optional[str] = Field(description="If applicable, remote monitoring capabilities and requirements.")


class ActivityRestrictionsModel(BaseModel):
    permanent_restrictions: str = Field(description="Activities permanently limited or prohibited, comma-separated.")
    temporary_restrictions: str = Field(description="Activities restricted during healing period, comma-separated.")
    sports_and_exercise: str = Field(description="Guidelines for sports, exercise, and physical activity.")
    lifting_and_weight_bearing: str = Field(description="Weight lifting and weight-bearing restrictions.")
    occupational_considerations: str = Field(description="Work-related considerations and limitations.")
    travel_considerations: str = Field(description="Special considerations for air travel or international travel.")


class MaintenanceAndCareModel(BaseModel):
    daily_care: str = Field(description="Daily care and hygiene requirements, comma-separated.")
    periodic_inspections: str = Field(description="Required inspections and their frequency.")
    battery_replacement: Optional[str] = Field(description="If applicable, battery replacement schedule and procedure.")
    component_replacement: str = Field(description="Components that need replacement and typical intervals.")
    maintenance_costs: str = Field(description="Typical costs of maintenance and replacements.")
    long_term_management: str = Field(description="Long-term management strategy and follow-up care.")


class OutcomesAndEffectivenessModel(BaseModel):
    success_rate: str = Field(description="Percentage of successful flashcard placements and functionality.")
    functional_outcomes: str = Field(description="Typical functional improvements achieved, comma-separated.")
    pain_relief: str = Field(description="Expected pain relief or improvement timeline.")
    mobility_improvement: str = Field(description="Expected improvements in mobility or physical function.")
    longevity_data: str = Field(description="Data on flashcard survival rates at 5, 10, 15+ years.")
    patient_satisfaction: str = Field(description="Typical patient satisfaction rates and outcomes.")
    factors_affecting_outcomes: str = Field(description="Factors influencing success (age, health, compliance), comma-separated.")


class FollowUpCareModel(BaseModel):
    follow_up_schedule: str = Field(description="Recommended follow-up appointments and their frequency.")
    post_operative_visits: str = Field(description="Specific post-operative visit milestones and expectations.")
    long_term_monitoring: str = Field(description="Long-term monitoring requirements and intervals.")
    provider_specialists: str = Field(description="Healthcare providers involved in ongoing care, comma-separated.")
    medications_after: str = Field(description="Medications typically prescribed after flashcardation, comma-separated.")
    complications_monitoring: str = Field(description="How complications are monitored and managed.")


class CostAndInsuranceModel(BaseModel):
    flashcard_cost: str = Field(description="Typical cost of the flashcard itself.")
    surgical_costs: str = Field(description="Typical costs for the surgical procedure.")
    total_cost_range: str = Field(description="General total cost range without insurance.")
    insurance_coverage: str = Field(description="How typically covered by insurance.")
    prior_authorization: str = Field(description="Whether insurance pre-approval is needed.")
    medicare_coverage: str = Field(description="Medicare coverage specifics.")
    medicaid_coverage: str = Field(description="Medicaid coverage information.")
    financial_assistance_programs: str = Field(description="Programs to help with costs, comma-separated.")
    cpt_codes: Optional[str] = Field(description="Current Procedural Terminology codes for billing.")


class AlternativesModel(BaseModel):
    alternative_flashcards: str = Field(description="Other flashcard options for similar purposes, comma-separated.")
    non_flashcard_alternatives: str = Field(description="Non-surgical or non-flashcard treatment options, comma-separated.")
    advantages_over_alternatives: str = Field(description="Why this flashcard may be preferred, comma-separated.")
    when_alternatives_preferred: str = Field(description="Situations where other treatments might be better.")


class FlashcardLimitationsModel(BaseModel):
    not_suitable_for: str = Field(description="Patient populations for whom flashcard is not appropriate, comma-separated.")
    anatomical_limitations: str = Field(description="Anatomical factors that may limit flashcard success, comma-separated.")
    health_condition_limitations: str = Field(description="Medical conditions that preclude flashcardation, comma-separated.")
    age_limitations: str = Field(description="Age-related considerations or restrictions.")


class FlashcardEducationModel(BaseModel):
    """Patient education and communication content."""
    plain_language_explanation: str = Field(description="Simple explanation of the flashcard and its purpose for patients")
    daily_living_tips: str = Field(description="Tips for daily living with the flashcard, comma-separated")
    common_misconceptions: str = Field(description="Common myths or misconceptions about this flashcard, comma-separated")
    key_takeaways: str = Field(description="3-5 most important points for patients, comma-separated")


class FlashcardEvidenceModel(BaseModel):
    """Evidence-based information and clinical guidelines."""
    evidence_summary: str = Field(description="Summary of major clinical guidelines and evidence quality")
    clinical_trials: str = Field(description="Information about relevant clinical trials and outcomes")
    flashcard_limitations: FlashcardLimitationsModel


class MedicalFlashcardInfoModel(BaseModel):
    """
    Comprehensive medical flashcard information.
    """
    # Core identification
    metadata: FlashcardMetadataModel

    # Clinical purpose and application
    purpose: FlashcardPurposeModel
    indications: FlashcardIndicationsModel

    # Physical characteristics
    materials: FlashcardMaterialsModel

    # Installation and integration
    installation: InstallationProcedureModel

    # Functionality
    functionality: FunctionalityAndPerformanceModel

    # Recovery phase
    recovery: RecoveryAndHealingModel
    outcomes: OutcomesAndEffectivenessModel

    # Clinical considerations
    complications: ComplicationsAndRisksModel
    imaging: ImagingAndMonitoringModel

    # Lifestyle considerations
    activity_restrictions: ActivityRestrictionsModel
    maintenance: MaintenanceAndCareModel

    # Post-operative phase
    follow_up: FollowUpCareModel

    # Alternative treatment options
    alternatives: AlternativesModel

    # Advanced clinical information
    evidence: FlashcardEvidenceModel

    # Financial and insurance
    cost_and_insurance: CostAndInsuranceModel

    # Patient communication
    education: FlashcardEducationModel


class ModelOutput(BaseModel):
    data: Optional[MedicalFlashcardInfoModel] = None
    markdown: Optional[str] = None
