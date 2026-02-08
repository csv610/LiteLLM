"""
sane_interview_models.py - Pydantic models for SANE interview data structures

Defines comprehensive data models for Sexual Assault Nurse Examiner (SANE) interviews
with trauma-informed approach and proper data validation.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class YesNoUnsure(str, Enum):
    YES = "yes"
    NO = "no"
    UNSURE = "unsure"
    DECLINE = "decline_to_answer"
    EXPLAIN = "explain"


class SexualContactType(str, Enum):
    VAGINAL = "vaginal"
    ORAL = "oral"
    ANAL = "anal"
    DIGITAL = "digital"
    OTHER = "other"


class PainLevel(int, Enum):
    NONE = 0
    MINIMAL = 1
    MILD = 3
    MODERATE = 5
    SEVERE = 7
    WORST = 10


# 1. Introduction and Consent
class ConsentSection(BaseModel):
    understands_purpose: Optional[YesNoUnsure] = None
    wants_explanation: Optional[YesNoUnsure] = None
    gives_permission: Optional[YesNoUnsure] = None
    additional_information: Optional[str] = None
    wants_advocate_present: Optional[YesNoUnsure] = None
    advocate_name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=150, description="Patient age in years")
    sex: Optional[str] = Field(None, description="Biological sex for medical assessment")
    gender_identity: Optional[str] = Field(None, description="Gender identity (optional)")


# 2. General Medical History
class MedicalHistory(BaseModel):
    medical_conditions: Optional[str] = None
    current_medications: Optional[str] = None
    allergies: Optional[str] = None
    last_menstrual_period: Optional[str] = None
    pregnancy_history: Optional[str] = None
    currently_pregnant: Optional[YesNoUnsure] = None


# 3. Incident History
class IncidentHistory(BaseModel):
    narrative: Optional[str] = Field(None, description="Survivor's own words")
    incident_date: Optional[str] = None
    incident_time: Optional[str] = None
    location: Optional[str] = None
    knows_assailant: Optional[YesNoUnsure] = None
    number_of_individuals: Optional[int] = None
    weapons_used: Optional[YesNoUnsure] = None
    weapon_details: Optional[str] = None
    physically_restrained: Optional[YesNoUnsure] = None
    restraint_details: Optional[str] = None
    lost_consciousness: Optional[YesNoUnsure] = None
    forced_substances: Optional[YesNoUnsure] = None
    substance_details: Optional[str] = None
    witnesses: Optional[YesNoUnsure] = None
    witness_details: Optional[str] = None


# 4. Sexual Contact Details
class SexualContactDetails(BaseModel):
    contact_types: Optional[List[SexualContactType]] = None
    condom_used: Optional[YesNoUnsure] = None
    ejaculation_noted: Optional[YesNoUnsure] = None
    ejaculation_location: Optional[str] = None
    objects_used: Optional[YesNoUnsure] = None
    object_details: Optional[str] = None
    able_to_resist: Optional[YesNoUnsure] = None
    resistance_details: Optional[str] = None
    clothing_removed_torn: Optional[YesNoUnsure] = None
    post_incident_activities: Optional[List[str]] = Field(
        None, 
        description="bathed, changed clothes, urinated, eaten, brushed teeth, etc."
    )
    items_cleaned_disposed: Optional[YesNoUnsure] = None


# 5. Injury and Pain Assessment
class InjuryAssessment(BaseModel):
    has_pain: Optional[YesNoUnsure] = None
    pain_locations: Optional[str] = None
    pain_level: Optional[int] = Field(None, ge=0, le=10)
    physical_assault_types: Optional[List[str]] = Field(
        None,
        description="hit, slap, kick, bite, strangle, etc."
    )
    visible_injuries: Optional[str] = None
    symptoms: Optional[List[str]] = Field(
        None,
        description="dizzy, nauseous, headache, etc."
    )
    genital_anal_symptoms: Optional[str] = None


# 6. Forensic Evidence Collection
class ForensicEvidence(BaseModel):
    urinated_since: Optional[YesNoUnsure] = None
    defecated_since: Optional[YesNoUnsure] = None
    changed_sanitary_products: Optional[YesNoUnsure] = None
    eaten_drunk_smoked: Optional[YesNoUnsure] = None
    items_left_behind: Optional[YesNoUnsure] = None
    items_description: Optional[str] = None
    wearing_same_clothes: Optional[YesNoUnsure] = None
    wants_items_collected: Optional[YesNoUnsure] = None


# 7. Prophylaxis and Treatment
class TreatmentDiscussion(BaseModel):
    accepts_sti_prophylaxis: Optional[YesNoUnsure] = None
    wants_emergency_contraception: Optional[YesNoUnsure] = None
    recent_hiv_test: Optional[YesNoUnsure] = None
    wants_hiv_test: Optional[YesNoUnsure] = None
    medication_concerns: Optional[str] = None


# 8. Emotional and Psychological Assessment
class PsychologicalAssessment(BaseModel):
    current_emotional_state: Optional[str] = None
    has_trusted_support: Optional[YesNoUnsure] = None
    support_person_details: Optional[str] = None
    previous_trauma: Optional[YesNoUnsure] = None
    feels_safe_going_home: Optional[YesNoUnsure] = None
    wants_counselor: Optional[YesNoUnsure] = None


# 9. Legal and Follow-Up
class LegalFollowUp(BaseModel):
    reported_to_police: Optional[YesNoUnsure] = None
    wants_reporting_explanation: Optional[YesNoUnsure] = None
    wants_evidence_collected: Optional[YesNoUnsure] = None
    contact_for_followup: Optional[YesNoUnsure] = None
    contact_information: Optional[str] = None
    needs_transportation: Optional[YesNoUnsure] = None
    needs_safe_housing: Optional[YesNoUnsure] = None


# 10. Closure and Support
class ClosureSupport(BaseModel):
    additional_questions: Optional[str] = None
    wants_next_steps_review: Optional[YesNoUnsure] = None
    wants_resources_explained: Optional[YesNoUnsure] = None


# Complete Interview Record
class SANEInterviewRecord(BaseModel):
    interview_date: datetime = Field(default_factory=datetime.now)
    interviewer_name: Optional[str] = None
    patient_id: Optional[str] = Field(None, description="Use anonymous identifier")
    
    consent: ConsentSection = Field(default_factory=ConsentSection)
    medical_history: MedicalHistory = Field(default_factory=MedicalHistory)
    incident_history: IncidentHistory = Field(default_factory=IncidentHistory)
    sexual_contact: SexualContactDetails = Field(default_factory=SexualContactDetails)
    injury_assessment: InjuryAssessment = Field(default_factory=InjuryAssessment)
    forensic_evidence: ForensicEvidence = Field(default_factory=ForensicEvidence)
    treatment: TreatmentDiscussion = Field(default_factory=TreatmentDiscussion)
    psychological: PsychologicalAssessment = Field(default_factory=PsychologicalAssessment)
    legal_followup: LegalFollowUp = Field(default_factory=LegalFollowUp)
    closure: ClosureSupport = Field(default_factory=ClosureSupport)
    
    additional_notes: Optional[str] = None
