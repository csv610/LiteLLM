from pydantic import BaseModel, Field
from typing import Optional

class ProcedurePurpose(BaseModel):
    primary_purpose: str = Field(description="Main reason this procedure is performed.")
    therapeutic_uses: str = Field(description="Specific conditions or diseases this procedure treats, comma-separated.")
    diagnostic_uses: str = Field(description="Diagnostic purposes of this procedure, comma-separated.")
    preventive_uses: str = Field(description="Preventive health applications of this procedure.")

class ProcedureIndications(BaseModel):
    when_recommended: str = Field(description="Clinical situations when this procedure is typically recommended, comma-separated.")
    symptoms_requiring_procedure: str = Field(description="Symptoms that lead doctors to recommend this procedure, comma-separated.")
    conditions_treated: str = Field(description="Medical conditions this procedure addresses, comma-separated.")
    contraindications: str = Field(description="Conditions that make this procedure unsafe or inappropriate, comma-separated.")

class PreparationRequirements(BaseModel):
    fasting_required: str = Field(description="Whether fasting is needed and for how long.")
    medication_adjustments: str = Field(description="Medications to stop or adjust before procedure, comma-separated.")
    dietary_restrictions: str = Field(description="Foods or drinks to avoid before procedure, comma-separated.")
    pre_procedure_tests: str = Field(description="Required tests or evaluations before procedure, comma-separated.")
    items_to_bring: str = Field(description="What to bring to the procedure appointment, comma-separated.")
    lifestyle_modifications: str = Field(description="Activities to avoid before procedure (smoking, alcohol, exercise), comma-separated.")

class ProcedureDetails(BaseModel):
    procedure_type: str = Field(description="Type of procedure (surgical, minimally invasive, endoscopic, etc).")
    anesthesia_type: str = Field(description="Type of anesthesia used (general, local, sedation, regional).")
    step_by_step_process: str = Field(description="Detailed steps of how the procedure is performed, numbered or comma-separated.")
    duration: str = Field(description="How long the procedure takes from start to finish.")
    location: str = Field(description="Where the procedure is typically performed (hospital, outpatient center, clinic).")
    equipment_used: str = Field(description="Medical equipment and instruments used, comma-separated.")
    hospital_stay: str = Field(description="Whether hospitalization is required and for how long.")

class DiscomfortAndRisks(BaseModel):
    discomfort_level: str = Field(description="Expected level of pain or discomfort during and after procedure.")
    common_sensations: str = Field(description="What patients typically feel during procedure, comma-separated.")
    common_side_effects: str = Field(description="Temporary side effects that are normal, comma-separated.")
    serious_risks: str = Field(description="Rare but serious complications to be aware of, comma-separated.")
    complication_rates: str = Field(description="Statistical rates of major complications.")
    mortality_risk: Optional[str] = Field(description="Risk of death from procedure if applicable.")

class RecoveryInformation(BaseModel):
    immediate_recovery: str = Field(description="What to expect immediately after procedure.")
    recovery_timeline: str = Field(description="Typical recovery milestones and duration.")
    pain_management: str = Field(description="How pain is managed during recovery, comma-separated.")
    activity_restrictions: str = Field(description="Physical limitations during recovery period, comma-separated.")
    return_to_work: str = Field(description="When patients can typically return to work.")
    return_to_normal_activities: str = Field(description="When patients can resume normal activities.")
    warning_signs: str = Field(description="Symptoms requiring immediate medical attention, comma-separated.")

class OutcomesAndEffectiveness(BaseModel):
    success_rate: str = Field(description="Percentage of successful outcomes.")
    expected_benefits: str = Field(description="What patients can expect to gain from procedure, comma-separated.")
    symptom_improvement: str = Field(description="How symptoms typically improve after procedure.")
    long_term_outcomes: str = Field(description="Long-term results and durability of procedure.")
    factors_affecting_outcomes: str = Field(description="Patient or clinical factors that influence success, comma-separated.")

class FollowUpCare(BaseModel):
    follow_up_schedule: str = Field(description="When and how often follow-up appointments are needed.")
    monitoring_required: str = Field(description="Tests or evaluations needed after procedure, comma-separated.")
    lifestyle_changes: str = Field(description="Permanent lifestyle modifications recommended, comma-separated.")
    medications_after: str = Field(description="Medications typically prescribed after procedure, comma-separated.")
    physical_therapy: str = Field(description="Whether physical therapy or rehabilitation is needed.")

class CostAndInsurance(BaseModel):
    typical_cost_range: str = Field(description="General cost range without insurance.")
    insurance_coverage: str = Field(description="How typically covered by insurance.")
    prior_authorization: str = Field(description="Whether insurance pre-approval is needed.")
    medicare_coverage: str = Field(description="Medicare coverage specifics.")
    medicaid_coverage: str = Field(description="Medicaid coverage information.")
    financial_assistance_programs: str = Field(description="Programs to help with costs, comma-separated.")
    cpt_codes: Optional[str] = Field(description="Current Procedural Terminology codes for billing.")

class Alternatives(BaseModel):
    alternative_procedures: str = Field(description="Other procedures that achieve similar goals, comma-separated.")
    non_surgical_alternatives: str = Field(description="Non-invasive treatment options, comma-separated.")
    advantages_over_alternatives: str = Field(description="Why this procedure may be preferred, comma-separated.")
    when_alternatives_preferred: str = Field(description="Clinical scenarios where other treatments are better, comma-separated.")

class TechnicalDetails(BaseModel):
    surgical_approach: str = Field(description="Surgical technique and approach used.")
    technology_used: str = Field(description="Advanced technology or robotics involved.")
    procedure_variations: str = Field(description="Different variations or modifications of the procedure, comma-separated.")
    surgeon_qualifications: str = Field(description="Required training and certifications for performing surgeon.")
    facility_requirements: str = Field(description="Hospital or facility requirements for performing procedure.")

class ProcedureLimitations(BaseModel):
    not_suitable_for: str = Field(description="Patient populations for whom procedure is not appropriate, comma-separated.")
    age_limitations: str = Field(description="Age-related considerations or restrictions.")
    medical_conditions_precluding: str = Field(description="Medical conditions that prevent procedure, comma-separated.")
    anatomical_limitations: str = Field(description="Anatomical factors that may limit procedure success, comma-separated.")

class ProcedureMetadata(BaseModel):
    """Basic information about the procedure."""
    procedure_name: str = Field(description="Official name of the procedure")
    alternative_names: str = Field(description="Other names for this procedure, comma-separated")
    procedure_category: str = Field(description="Category (surgical, minimally invasive, diagnostic, etc)")
    medical_specialty: str = Field(description="Primary medical specialties, comma-separated")

class ProcedureEducation(BaseModel):
    """Patient education and communication content."""
    plain_language_explanation: str = Field(description="Simple explanation for patients")
    key_takeaways: str = Field(description="3-5 most important points, comma-separated")
    common_misconceptions: str = Field(description="Common myths about this procedure, comma-separated")

class ProcedureEvidence(BaseModel):
    """Evidence-based information and clinical guidelines."""
    evidence_summary: str = Field(description="Summary of major guidelines and evidence quality")
    procedure_limitations: ProcedureLimitations

class ProcedureInfo(BaseModel):
    """
    Comprehensive medical procedure information.
    """
    metadata: ProcedureMetadata
    purpose: ProcedurePurpose
    indications: ProcedureIndications
    preparation: PreparationRequirements
    details: ProcedureDetails
    risks: DiscomfortAndRisks
    recovery: RecoveryInformation
    outcomes: OutcomesAndEffectiveness
    follow_up: FollowUpCare
    alternatives: Alternatives
    technical: TechnicalDetails
    evidence: ProcedureEvidence
    cost_and_insurance: CostAndInsurance
    education: ProcedureEducation
