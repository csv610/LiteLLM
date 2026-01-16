"""
Lungs and Chest Assessment

Evaluate patient respiratory status through physical examination including
vital signs, auscultation, percussion, chest expansion, and sputum analysis.
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
    blood_pressure: str = Field(..., description="BP in mmHg")
    respiratory_rate: int = Field(..., description="Breaths per minute")
    oxygen_saturation: float = Field(..., description="O2 saturation percentage")

class Auscultation(BaseModel):
    R_upper: str
    R_mid: str
    R_lower: str
    L_upper: str
    L_mid: str
    L_lower: str

class Percussion(BaseModel):
    R_upper: str
    R_mid: str
    R_lower: str
    L_upper: str
    L_mid: str
    L_lower: str

class Sputum(BaseModel):
    color: str
    amount_ml: float
    sample_id: str
    smell: Optional[str] = None

class Media(BaseModel):
    chest_video: Optional[str] = None
    ausc_audio: Optional[str] = None

class NurseReport(BaseModel):
    vitals: Vitals
    auscultation: Auscultation
    percussion: Percussion
    chest_expansion: str
    sputum: Optional[Sputum] = None
    media: Optional[Media] = None

# ----------------------------
# 3. LLM Assessment Model
# ----------------------------
class LLMAssessment(BaseModel):
    primary_impression: str = Field(..., description="Primary impression from LLM")
    urgency: Literal["normal", "monitor", "urgent", "emergency"] = Field(..., description="Triage urgency level")
    recommendations: List[str] = Field(..., description="Recommended clinical actions")
    confidence: Optional[float] = Field(None, description="Confidence of the assessment")

class LungsChestExam(BaseModel):
    patient_id: str = Field(..., description="Patient unique identifier")
    encounter_id: str = Field(..., description="Encounter unique identifier")
    timestamp: datetime = Field(default_factory=datetime.now, description="Assessment timestamp")
    patient_answers: Optional[List[PatientAnswer]] = Field(None, description="Patient answers")
    nurse_report: NurseReport = Field(..., description="Nurse examination findings")
    llm_assessment: Optional[LLMAssessment] = Field(None, description="AI-generated assessment")

if __name__ == '__main__':
    print("Lungs and Chest Exam module loaded successfully")
