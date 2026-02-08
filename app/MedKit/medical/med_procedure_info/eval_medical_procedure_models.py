from pydantic import BaseModel, Field
from typing import List, Optional

class MedicalAccuracy(BaseModel):
    score: int = Field(description="Score from 1-10 regarding medical accuracy.")
    inaccuracies: List[str] = Field(description="List of specific medical inaccuracies found, if any.")
    missing_critical_info: List[str] = Field(description="List of critical medical information that is missing.")

class SafetyCheck(BaseModel):
    score: int = Field(description="Score from 1-10 regarding patient safety information.")
    contraindications_check: str = Field(description="Evaluation of how well contraindications are covered.")
    risk_assessment: str = Field(description="Evaluation of how well risks and complications are described.")
    safety_warnings: List[str] = Field(description="List of missing safety warnings.")

class ClarityAndUsability(BaseModel):
    score: int = Field(description="Score from 1-10 regarding clarity and usability for the target audience.")
    jargon_usage: str = Field(description="Assessment of medical jargon usage - is it appropriate or too complex?")
    structure_feedback: str = Field(description="Feedback on the structure and flow of the information.")

class EvidenceBasedReview(BaseModel):
    score: int = Field(description="Score from 1-10 regarding adherence to evidence-based practices.")
    outdated_practices: List[str] = Field(description="List of any outdated practices mentioned.")
    guideline_alignment: str = Field(description="How well the content aligns with standard medical guidelines.")

class MedicalProcedureEvaluationModel(BaseModel):
    """
    Critical evaluation of medical procedure information.
    """
    procedure_name: str = Field(description="Name of the procedure being evaluated.")
    overall_score: int = Field(description="Overall quality score from 1-10.")
    executive_summary: str = Field(description="High-level summary of the evaluation.")
    accuracy: MedicalAccuracy
    safety: SafetyCheck
    clarity: ClarityAndUsability
    evidence_check: EvidenceBasedReview
    recommendations: List[str] = Field(description="Specific actionable recommendations for improvement.")

class ModelOutput(BaseModel):
    data: Optional[MedicalProcedureEvaluationModel] = None
    markdown: Optional[str] = None
