from pydantic import BaseModel, Field
from enum import Enum
from dataclasses import dataclass

from typing import List, Optional

class HistoryPurpose(str, Enum):
    SURGERY = "surgery"
    MEDICATION = "medication"
    PHYSICAL_EXAM = "physical_exam"

class QuestionRequirement(str, Enum):
    MANDATORY = "mandatory"
    OPTIONAL = "optional"

class FollowUpQuestionModel(BaseModel):
    question: str = Field(description="The follow-up question text")
    clinical_reason: str = Field(description="Why this follow-up is clinically important")
    investigation_focus: str = Field(description="What specific diagnostic or clinical aspect is being investigated")

class HistoryQuestionModel(BaseModel):
    question: str = Field(description="The question to ask the patient")
    clinical_relevance: str = Field(description="Why this question is clinically relevant")
    requirement: QuestionRequirement = Field(description="Whether mandatory or optional")
    expected_answer_type: str = Field(description="Type of answer expected (yes/no, descriptive, date, etc.)")

class PastConditionQuestionModel(HistoryQuestionModel):
    condition_category: str = Field(description="Category of condition (cardiac, respiratory, endocrine, etc.)")
    follow_up_questions: List[FollowUpQuestionModel] = Field(default_factory=list)

class HospitalizationQuestionModel(HistoryQuestionModel):
    scope: str = Field(description="Scope of hospitalization question (frequency, reason, duration, etc.)")
    follow_up_questions: List[FollowUpQuestionModel] = Field(default_factory=list)

class SurgeryQuestionModel(HistoryQuestionModel):
    detail_level: str = Field(description="Level of detail requested (list, specific procedures, complications)")
    follow_up_questions: List[FollowUpQuestionModel] = Field(default_factory=list)

class FamilyHistoryQuestionModel(HistoryQuestionModel):
    family_member_type: str = Field(description="Type of family member (parent, sibling, grandparent, etc.)")
    condition_focus: str = Field(description="Medical conditions to focus on")
    follow_up_questions: List[FollowUpQuestionModel] = Field(default_factory=list)

class MedicationQuestionModel(HistoryQuestionModel):
    aspect: str = Field(description="Aspect of medication use (current medications, dosage, adherence, side effects)")
    follow_up_questions: List[FollowUpQuestionModel] = Field(default_factory=list)

class AllergyQuestionModel(HistoryQuestionModel):
    allergy_type: str = Field(description="Type of allergy (medication, food, environmental, latex, contrast dye)")
    detail_aspect: str = Field(description="Aspect of allergy to assess (type, reaction, severity, management)")
    follow_up_questions: List[FollowUpQuestionModel] = Field(default_factory=list)

class VaccinationQuestionModel(HistoryQuestionModel):
    vaccine_focus: str = Field(description="Specific vaccine or vaccine category")
    follow_up_questions: List[FollowUpQuestionModel] = Field(default_factory=list)

class LifestyleQuestionModel(HistoryQuestionModel):
    category: str = Field(description="Lifestyle category (tobacco, alcohol, diet, exercise, sleep, stress)")
    detail_requested: str = Field(description="Type of detail requested (frequency, quantity, impact, duration)")
    follow_up_questions: List[FollowUpQuestionModel] = Field(default_factory=list)

class PersonalSocialQuestionModel(HistoryQuestionModel):
    social_aspect: str = Field(description="Social aspect (occupation, housing, relationships, education, support systems)")
    follow_up_questions: List[FollowUpQuestionModel] = Field(default_factory=list)

class PastMedicalHistoryQuestionsModel(BaseModel):
    condition_questions: List[PastConditionQuestionModel]
    hospitalization_questions: List[HospitalizationQuestionModel]
    surgery_questions: List[SurgeryQuestionModel]

class FamilyHistoryQuestionsModel(BaseModel):
    maternal_history_questions: List[FamilyHistoryQuestionModel]
    paternal_history_questions: List[FamilyHistoryQuestionModel]
    genetic_risk_questions: List[FamilyHistoryQuestionModel]

class DrugInformationQuestionsModel(BaseModel):
    medication_questions: List[MedicationQuestionModel]
    allergy_questions: List[AllergyQuestionModel]
    adverse_reaction_questions: List[AllergyQuestionModel]

class VaccinationQuestionsModel(BaseModel):
    vaccination_status_questions: List[VaccinationQuestionModel]
    vaccine_specific_questions: List[VaccinationQuestionModel]
    booster_questions: List[VaccinationQuestionModel]

class LifestyleAndSocialQuestionsModel(BaseModel):
    lifestyle_questions: List[LifestyleQuestionModel]
    personal_social_questions: List[PersonalSocialQuestionModel]

class PatientMedicalHistoryModel(BaseModel):
    purpose: str
    exam: str
    age: int
    gender: str
    past_medical_history: PastMedicalHistoryQuestionsModel
    family_history: FamilyHistoryQuestionsModel
    drug_information: DrugInformationQuestionsModel
    vaccination: VaccinationQuestionsModel
    lifestyle_and_social: LifestyleAndSocialQuestionsModel


class ModelOutput(BaseModel):
    data: Optional[PatientMedicalHistoryModel] = None
    markdown: Optional[str] = None
