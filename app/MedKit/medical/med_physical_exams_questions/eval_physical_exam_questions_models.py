"""Pydantic models for physical exam question evaluation."""

from typing import List, Literal
from pydantic import BaseModel


class CriteriaEvaluation(BaseModel):
    criterion: str
    score: float
    max_score: float
    feedback: str
    status: Literal["pass", "warning", "fail"]


class QuestionEvaluation(BaseModel):
    question_id: int
    question_text: str
    clarity_score: float
    clinical_relevance_score: float
    appropriateness_score: float
    overall_quality: float
    feedback: str


class SectionEvaluation(BaseModel):
    section_name: str
    question_count: int
    expected_count: str
    sufficiency_status: Literal["adequate", "insufficient", "excessive"]
    average_quality_score: float
    clinical_standards_score: float
    feedback: str


class QualityEvaluation(BaseModel):
    exam_name: str = "Unknown Exam"
    overall_quality_score: float
    medical_standards_compliance: float
    question_sufficiency: float
    relevancy_score: float
    accuracy_score: float
    cultural_sensitivity_score: float
    trauma_informed_score: float
    section_evaluations: List[SectionEvaluation] = []
    criteria_evaluations: List[CriteriaEvaluation] = []
    strengths: List[str]
    areas_for_improvement: List[str]
    recommendations: List[str]
    pass_fail: Literal["pass", "conditional_pass", "fail"]
