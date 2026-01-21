from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class HistoryPurpose(str, Enum):
    SURGERY = "surgery"
    MEDICATION = "medication"
    PHYSICAL_EXAM = "physical_exam"

class QuestionRequirement(str, Enum):
    MANDATORY = "mandatory"
    OPTIONAL = "optional"

class FollowUpQuestion(BaseModel):
    question: str = Field(description="The follow-up question text")
    clinical_reason: str = Field(description="Why this follow-up is clinically important")
    investigation_focus: str = Field(description="What specific diagnostic or clinical aspect is being investigated")

class HistoryQuestion(BaseModel):
    question: str = Field(description="The question to ask the patient")
    clinical_relevance: str = Field(description="Why this question is clinically relevant")
    requirement: QuestionRequirement = Field(description="Whether mandatory or optional")
    expected_answer_type: str = Field(description="Type of answer expected (yes/no, descriptive, date, etc.)")

class PastConditionQuestion(HistoryQuestion):
    condition_category: str = Field(description="Category of condition (cardiac, respiratory, endocrine, etc.)")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

class HospitalizationQuestion(HistoryQuestion):
    scope: str = Field(description="Scope of hospitalization question (frequency, reason, duration, etc.)")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

class SurgeryQuestion(HistoryQuestion):
    detail_level: str = Field(description="Level of detail requested (list, specific procedures, complications)")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

class FamilyHistoryQuestion(HistoryQuestion):
    family_member_type: str = Field(description="Type of family member (parent, sibling, grandparent, etc.)")
    condition_focus: str = Field(description="Medical conditions to focus on")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

class MedicationQuestion(HistoryQuestion):
    aspect: str = Field(description="Aspect of medication use (current medications, dosage, adherence, side effects)")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

class AllergyQuestion(HistoryQuestion):
    allergy_type: str = Field(description="Type of allergy (medication, food, environmental, latex, contrast dye)")
    detail_aspect: str = Field(description="Aspect of allergy to assess (type, reaction, severity, management)")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

class VaccinationQuestion(HistoryQuestion):
    vaccine_focus: str = Field(description="Specific vaccine or vaccine category")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

class LifestyleQuestion(HistoryQuestion):
    category: str = Field(description="Lifestyle category (tobacco, alcohol, diet, exercise, sleep, stress)")
    detail_requested: str = Field(description="Type of detail requested (frequency, quantity, impact, duration)")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

class PersonalSocialQuestion(HistoryQuestion):
    social_aspect: str = Field(description="Social aspect (occupation, housing, relationships, education, support systems)")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

class PastMedicalHistoryQuestions(BaseModel):
    condition_questions: List[PastConditionQuestion]
    hospitalization_questions: List[HospitalizationQuestion]
    surgery_questions: List[SurgeryQuestion]

class FamilyHistoryQuestions(BaseModel):
    maternal_history_questions: List[FamilyHistoryQuestion]
    paternal_history_questions: List[FamilyHistoryQuestion]
    genetic_risk_questions: List[FamilyHistoryQuestion]

class DrugInformationQuestions(BaseModel):
    medication_questions: List[MedicationQuestion]
    allergy_questions: List[AllergyQuestion]
    adverse_reaction_questions: List[AllergyQuestion]

class VaccinationQuestions(BaseModel):
    vaccination_status_questions: List[VaccinationQuestion]
    vaccine_specific_questions: List[VaccinationQuestion]
    booster_questions: List[VaccinationQuestion]

class LifestyleAndSocialQuestions(BaseModel):
    lifestyle_questions: List[LifestyleQuestion]
    personal_social_questions: List[PersonalSocialQuestion]

class PatientMedicalHistoryQuestions(BaseModel):
    purpose: str
    exam: str
    age: int
    gender: str
    past_medical_history: PastMedicalHistoryQuestions
    family_history: FamilyHistoryQuestions
    drug_information: DrugInformationQuestions
    vaccination: VaccinationQuestions
    lifestyle_and_social: LifestyleAndSocialQuestions
