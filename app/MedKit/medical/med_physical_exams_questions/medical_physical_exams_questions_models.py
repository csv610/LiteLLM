from pydantic import BaseModel, Field
from typing import List, Optional

class ExamQuestions(BaseModel):
    """Structured physical examination questions organized by technique."""
    exam_type: str = Field(description="Type of physical exam (e.g., Cardiovascular, Respiratory, Abdominal)")
    age: Optional[int] = Field(default=None, description="Age of the patient in years")
    gender: Optional[str] = Field(default=None, description="Gender of the patient (e.g., Male, Female, Other)")
    inspection_questions: List[str] = Field(
        default_factory=list,
        description="Questions related to visual inspection of the patient and affected area"
    )
    palpation_questions: List[str] = Field(
        default_factory=list,
        description="Questions related to physical palpation and touch assessment"
    )
    percussion_questions: List[str] = Field(
        default_factory=list,
        description="Questions related to percussion technique and findings"
    )
    auscultation_questions: List[str] = Field(
        default_factory=list,
        description="Questions related to listening with stethoscope"
    )
    verbal_assessment_questions: List[str] = Field(
        default_factory=list,
        description="Questions for verbal patient assessment and communication"
    )
    medical_history_questions: List[str] = Field(
        default_factory=list,
        description="Questions about past medical history relevant to this exam"
    )
    lifestyle_questions: List[str] = Field(
        default_factory=list,
        description="Questions about lifestyle factors that may affect findings"
    )
    family_history_questions: List[str] = Field(
        default_factory=list,
        description="Questions about family history relevant to this exam"
    )
