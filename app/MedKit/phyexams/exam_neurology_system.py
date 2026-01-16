"""
Neurology System Assessment

Evaluate patient neurological status through assessment of cranial nerves,
motor function, reflexes, coordination, sensory function, and gait.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

# ----------------------------
# 1. Pydantic Models
# ----------------------------
class PatientAnswer(BaseModel):
    question_id: str = Field(..., description="Unique identifier for the patient question")
    question_text: str = Field(..., description="Full text of the question asked to the patient")
    answer_text: str = Field(..., description="Patient's free-text response")
    answer_code: Optional[str] = Field(None, description="Structured code representing the type of answer")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score for the answer classification")

class NurseReport(BaseModel):
    vitals: dict = Field(..., description="Patient vital signs")
    cranial_nerves: dict = Field(..., description="Cranial nerve assessment")
    motor_exam: dict = Field(..., description="Motor strength and tone")
    reflexes: dict = Field(..., description="Deep tendon reflexes")
    coordination: dict = Field(..., description="Coordination tests")
    sensory_exam: dict = Field(..., description="Sensory function assessment")
    gait_balance: dict = Field(..., description="Gait and balance assessment")
    speech_language: str = Field(..., description="Speech observation")
    vision_pupils: str = Field(..., description="Vision and pupils observation")
    media: Optional[dict] = Field(None, description="Optional media files")

class LLMAssessment(BaseModel):
    primary_impression: str = Field(..., description="Primary impression from LLM")
    urgency: Literal["normal", "monitor", "urgent", "emergency"] = Field(..., description="Urgency level")
    recommendations: List[str] = Field(..., description="List of recommended clinical actions")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence of the assessment")

class NeurologyExam(BaseModel):
    patient_id: str = Field(..., description="Unique patient identifier")
    encounter_id: str = Field(..., description="Unique encounter identifier")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of assessment")
    patient_answers: Optional[List[PatientAnswer]] = Field(None, description="Patient answers to neurology questions")
    nurse_report: NurseReport = Field(..., description="Detailed neurology examination findings from the nurse")
    llm_assessment: Optional[LLMAssessment] = Field(None, description="AI-powered assessment and recommendations")

if __name__ == '__main__':
    print("Neurology System Exam module loaded successfully")
