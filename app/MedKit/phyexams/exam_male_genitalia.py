"""
Male Genitalia Examination Assessment

Evaluate male reproductive and urological health through physical examination
including inspection, palpation, hernia check, and urethral assessment.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

# ----------------------------
# 1. Pydantic Models
# ----------------------------
class PatientAnswer(BaseModel):
    question_id: str = Field(..., description="Unique patient question identifier")
    question_text: str = Field(..., description="Text of the question asked")
    answer_text: str = Field(..., description="Patient response")
    answer_code: Optional[str] = Field(None, description="LLM-coded response category")
    confidence: Optional[float] = Field(None, description="LLM confidence in coding")
    follow_up: Optional[List[str]] = Field(None, description="LLM-generated follow-up questions")

class NurseReport(BaseModel):
    inspection: dict = Field(..., description="Inspection of penis, scrotum, perineum")
    palpation: dict = Field(..., description="Palpation: testicular size, consistency, tenderness, masses")
    hernia_exam: dict = Field(..., description="Inguinal hernia check, reducibility, tenderness")
    urethral_exam: dict = Field(..., description="Urethral meatus inspection, discharge, lesions")
    media: Optional[dict] = Field(None, description="Optional images or videos for telemedicine")

class LLMAssessment(BaseModel):
    primary_impression: str = Field(..., description="Primary impression from LLM or clinical reasoning")
    urgency: Literal["normal", "monitor", "urgent", "emergency"] = Field(..., description="Triage urgency level")
    recommendations: List[str] = Field(..., description="Recommended clinical actions")
    confidence: Optional[float] = Field(None, description="Confidence of the assessment")

class MaleGenitaliaExam(BaseModel):
    patient_id: str = Field(..., description="Patient unique identifier")
    encounter_id: str = Field(..., description="Encounter unique identifier")
    timestamp: datetime = Field(default_factory=datetime.now, description="Assessment timestamp")
    patient_answers: Optional[List[PatientAnswer]] = Field(None, description="Patient answers to genital health questions")
    nurse_report: NurseReport = Field(..., description="Nurse examination findings")
    llm_assessment: Optional[LLMAssessment] = Field(None, description="AI-generated assessment")

if __name__ == '__main__':
    print("Male Genitalia Exam module loaded successfully")
