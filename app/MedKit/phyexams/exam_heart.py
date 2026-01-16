"""
Heart Examination Assessment

Evaluate patient cardiac status through physical examination including
vital signs, inspection, palpation, auscultation, and peripheral findings.
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

class Vitals(BaseModel):
    heart_rate: int = Field(..., description="Beats per minute")
    blood_pressure_systolic: int = Field(..., description="Systolic BP in mmHg")
    blood_pressure_diastolic: int = Field(..., description="Diastolic BP in mmHg")
    respiratory_rate: int = Field(..., description="Breaths per minute")
    oxygen_saturation: float = Field(..., description="O2 saturation percentage")
    temperature: Optional[float] = Field(None, description="Temperature in Celsius")

class NurseReport(BaseModel):
    vitals: dict = Field(..., description="Heart rate, blood pressure, respiratory rate, oxygen saturation")
    inspection: dict = Field(..., description="Observation: jugular venous distention, cyanosis, edema")
    palpation: dict = Field(..., description="Palpation: apex beat, thrills, heaves")
    auscultation: dict = Field(..., description="Heart sounds: S1, S2, murmurs, extra sounds")
    peripheral_signs: dict = Field(..., description="Peripheral pulses, capillary refill, edema")
    media: Optional[dict] = Field(None, description="Optional images or videos")

class LLMAssessment(BaseModel):
    primary_impression: str = Field(..., description="Primary impression from LLM")
    urgency: Literal["normal", "monitor", "urgent", "emergency"] = Field(..., description="Triage urgency level")
    recommendations: List[str] = Field(..., description="Recommended clinical actions")
    confidence: Optional[float] = Field(None, description="Confidence of the assessment")

class HeartExam(BaseModel):
    patient_id: str = Field(..., description="Patient unique identifier")
    encounter_id: str = Field(..., description="Encounter unique identifier")
    timestamp: datetime = Field(default_factory=datetime.now, description="Assessment timestamp")
    patient_answers: Optional[List[PatientAnswer]] = Field(None, description="Patient answers to heart-related questions")
    nurse_report: NurseReport = Field(..., description="Nurse examination findings")
    llm_assessment: Optional[LLMAssessment] = Field(None, description="AI-generated assessment")

if __name__ == '__main__':
    print("Heart Exam module loaded successfully")
