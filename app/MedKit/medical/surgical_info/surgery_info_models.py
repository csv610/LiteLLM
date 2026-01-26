"""Pydantic models for surgical procedure information structure."""

from pydantic import BaseModel, Field
from typing import Optional


class SurgeryMetadataModel(BaseModel):
    surgery_name: str = Field(description="Official name of the surgical procedure")
    alternative_names: str = Field(description="Other names for this surgery, comma-separated")
    procedure_code: str = Field(description="CPT or ICD procedure code")
    surgery_category: str = Field(description="Category of surgery (cardiovascular, orthopedic, gastrointestinal, etc.)")
    body_systems_involved: str = Field(description="Body systems affected by this surgery, comma-separated")

class SurgeryIndicationsModel(BaseModel):
    absolute_indications: str = Field(description="Conditions where surgery is mandatory or strongly indicated, comma-separated")
    relative_indications: str = Field(description="Conditions where surgery may be beneficial but alternatives exist, comma-separated")
    emergency_indications: str = Field(description="Life-threatening situations requiring immediate surgery, comma-separated")
    absolute_contraindications: str = Field(description="Conditions that completely prohibit the surgery, comma-separated")
    relative_contraindications: str = Field(description="Conditions that increase surgical risk but don't prohibit surgery, comma-separated")

class SurgeryBackgroundModel(BaseModel):
    definition: str = Field(description="Clear definition of what the surgery involves and why it's performed")
    surgical_anatomy: str = Field(description="Relevant anatomical structures and their relationships")
    historical_background: str = Field(description="Historical development of this surgical procedure")
    epidemiology: str = Field(description="How common this surgery is, indications prevalence, and population statistics")

class PreoperativePhaseModel(BaseModel):
    patient_evaluation: str = Field(description="Clinical examination and history taking requirements, comma-separated")
    laboratory_tests: str = Field(description="Required blood tests, urine tests, or other lab work, comma-separated")
    imaging_studies: str = Field(description="X-rays, CT scans, MRI, ultrasound needed before surgery, comma-separated")
    specialist_consultations: str = Field(description="Required consultations with other specialists, comma-separated")
    risk_stratification: str = Field(description="Tools and methods to assess surgical risk, comma-separated")
    preoperative_preparation: str = Field(description="Physical and mental preparation steps, comma-separated")
    patient_counseling_points: str = Field(description="Key discussion points with patient before surgery, comma-separated")

class OperativePhaseModel(BaseModel):
    surgical_approaches: str = Field(description="Open, laparoscopic, robotic, or other surgical approaches, comma-separated")
    anesthesia_type: str = Field(description="General, regional, local, or sedation requirements, comma-separated")
    patient_positioning: str = Field(description="How the patient is positioned during surgery")
    surgical_steps: str = Field(description="Step-by-step procedure description, numbered or comma-separated")
    instruments_equipment: str = Field(description="Special instruments or equipment needed, comma-separated")
    duration: str = Field(description="Typical duration of the surgical procedure")

class OperativeRisksModel(BaseModel):
    intraoperative_complications: str = Field(description="Complications that can occur during surgery, comma-separated")
    early_postoperative_complications: str = Field(description="Complications within first few days/weeks, comma-separated")
    late_postoperative_complications: str = Field(description="Long-term complications and sequelae, comma-separated")
    complication_rates: str = Field(description="Statistical rates of common complications")

class PostoperativePhaseModel(BaseModel):
    immediate_care: str = Field(description="ICU or recovery room management protocols, comma-separated")
    pain_management: str = Field(description="Analgesic protocols and pain control strategies, comma-separated")
    monitoring_parameters: str = Field(description="Vital signs and clinical parameters to monitor, comma-separated")
    diet_progression: str = Field(description="Dietary advancement plan after surgery, comma-separated")
    mobilization_protocol: str = Field(description="Timeline and steps for patient mobilization, comma-separated")
    drain_management: Optional[str] = Field(description="Management of surgical drains if applicable, comma-separated")
    hospital_stay: str = Field(description="Expected length of hospitalization")
    discharge_criteria: str = Field(description="Requirements for safe discharge from hospital, comma-separated")

class RecoveryAndOutcomesModel(BaseModel):
    recovery_timeline: str = Field(description="Recovery milestones and expected duration")
    rehabilitation_protocol: str = Field(description="Physical therapy or rehabilitation plan, comma-separated")
    return_to_work: str = Field(description="When patients can typically return to work")
    return_to_normal_activities: str = Field(description="When patients can resume normal activities")
    success_rates: str = Field(description="Statistical success rates of the procedure")
    functional_outcomes: str = Field(description="Expected functional recovery and quality of life, comma-separated")
    recurrence_rates: Optional[str] = Field(description="Rates of condition recurrence if applicable")
    long_term_outcomes: str = Field(description="Long-term results and patient outcomes, comma-separated")

class FollowUpModel(BaseModel):
    follow_up_schedule: str = Field(description="When and how often follow-up appointments are needed")
    monitoring_required: str = Field(description="Tests or evaluations needed after surgery, comma-separated")
    lifestyle_modifications: str = Field(description="Lifestyle changes and precautions needed after surgery, comma-separated")
    warning_signs: str = Field(description="Symptoms requiring immediate medical attention, comma-separated")

class AlternativesModel(BaseModel):
    medical_management: str = Field(description="Non-surgical treatment options, comma-separated")
    minimally_invasive_procedures: str = Field(description="Less invasive alternatives to open surgery, comma-separated")
    conservative_approaches: str = Field(description="Observation or expectant management options, comma-separated")
    advantages_over_alternatives: str = Field(description="Why this surgery may be preferred, comma-separated")

class TechnicalDetailsModel(BaseModel):
    surgical_approach_variations: str = Field(description="Different variations or modifications of the procedure, comma-separated")
    surgeon_qualifications: str = Field(description="Required training and certifications for performing surgeon")
    facility_requirements: str = Field(description="Hospital or facility requirements for performing procedure")
    technology_used: str = Field(description="Advanced technology or robotics involved")

class SurgeryResearchModel(BaseModel):
    recent_innovations: str = Field(description="New surgical techniques, technologies, or approaches developed in recent years, comma-separated")
    robotic_ai_applications: str = Field(description="Use of robotic surgery, AI assistance, or machine learning in this procedure, comma-separated")
    emerging_technologies: str = Field(description="New devices, instruments, or tools being developed or tested, comma-separated")
    clinical_trials: str = Field(description="Ongoing or recent clinical trials related to this surgery, comma-separated")
    future_directions: str = Field(description="Potential future developments and research areas, comma-separated")
    quality_improvement_initiatives: str = Field(description="Programs or protocols to improve surgical outcomes, comma-separated")

class SpecialPopulationsModel(BaseModel):
    pediatric_considerations: Optional[str] = Field(description="Special considerations for pediatric patients if applicable")
    geriatric_considerations: Optional[str] = Field(description="Special considerations for elderly patients")
    pregnancy_considerations: Optional[str] = Field(description="Safety and considerations during pregnancy if applicable")

class SurgeryEducationModel(BaseModel):
    plain_language_explanation: str = Field(description="Simple explanation of the surgery for patients")
    key_takeaways: str = Field(description="3-5 most important points about the surgery, comma-separated")
    common_misconceptions: str = Field(description="Common myths or misconceptions about this surgery, comma-separated")

class SurgeryEvidenceModel(BaseModel):
    evidence_level: str = Field(description="Level of evidence supporting this surgery (high, moderate, low)")
    evidence_summary: str = Field(description="Summary of major guidelines and evidence quality")
    comparative_effectiveness: Optional[str] = Field(description="Research comparing different surgical approaches or techniques")

class CostAndInsuranceModel(BaseModel):
    typical_cost_range: str = Field(description="General cost range without insurance")
    insurance_coverage: str = Field(description="How typically covered by insurance")
    medicare_coverage: str = Field(description="Medicare coverage specifics")
    medicaid_coverage: str = Field(description="Medicaid coverage information")
    prior_authorization: str = Field(description="Whether insurance pre-approval is needed")
    financial_assistance_programs: str = Field(description="Programs to help with costs, comma-separated")

class SurgeryInfoModel(BaseModel):
    metadata: SurgeryMetadataModel
    background: SurgeryBackgroundModel
    indications: SurgeryIndicationsModel
    preoperative: PreoperativePhaseModel
    operative: OperativePhaseModel
    operative_risks: OperativeRisksModel
    postoperative: PostoperativePhaseModel
    recovery_outcomes: RecoveryAndOutcomesModel
    follow_up: FollowUpModel
    alternatives: AlternativesModel
    special_populations: SpecialPopulationsModel
    technical: TechnicalDetailsModel
    research: SurgeryResearchModel
    evidence: SurgeryEvidenceModel
    education: SurgeryEducationModel
    cost_and_insurance: CostAndInsuranceModel


class ModelOutput(BaseModel):
    data: Optional[SurgeryInfoModel] = None
    markdown: Optional[str] = None
