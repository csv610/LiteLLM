"""
Musculoskeletal Exam - Core Business Logic (UI-Agnostic)

This module contains all exam logic, data structures, and processing.
It has ZERO dependencies on Streamlit, Gradio, or any UI framework.
Can be easily integrated with any UI framework.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Tuple

from pathlib import Path
from lite.utils import save_model_response


# ============================================================================
# DATA MODELS
# ============================================================================

class ExamAnswers(BaseModel):
    """All patient responses."""
    red_flags: Dict[str, str]
    medications: Dict[str, str]
    history: Dict[str, str]
    pain_assessment: Dict[str, str]
    functional: Dict[str, str]


class PhysicalExam(BaseModel):
    """Physical examination findings."""
    inspection: str
    palpation: str
    range_of_motion: str
    strength: str
    gait: str
    special_tests: str


class Assessment(BaseModel):
    """Clinical assessment."""
    red_flags: List[str]
    primary_impression: str
    urgency: str
    recommendations: List[str]


class PatientEducation(BaseModel):
    """Patient education responses."""
    diagnosis: str
    timeline: str
    permanent: str
    treatment: str
    alternatives: str
    activity: str
    prevention: str
    lifestyle: str
    complications: str
    specialist: str


class ExamRecord(BaseModel):
    """Complete exam record."""
    patient_name: str
    patient_id: str
    encounter_id: str
    timestamp: datetime
    answers: ExamAnswers
    physical_exam: PhysicalExam
    assessment: Assessment
    education: PatientEducation


# ============================================================================
# QUESTION DEFINITIONS (Data-only, no logic)
# ============================================================================

class QuestionSet:
    """All questions organized by category."""

    RED_FLAGS = [
        ("fever", "Fever, chills, or night sweats in past month?"),
        ("weight_loss", "Unexplained weight loss (>10 lbs) in past 3 months?"),
        ("neurologic", "Progressive numbness/weakness spreading down legs?"),
        ("bowel_bladder", "Changes in bowel/bladder control or saddle numbness?"),
        ("swelling_unilateral", "Severe one-sided leg swelling with calf pain?"),
        ("pain_rest", "Severe pain at rest that doesn't improve?"),
        ("trauma_high", "High-energy trauma, major fall, or MVA?"),
        ("systemic", "Rash, sore throat, recent infection, or constitutional symptoms?"),
    ]

    MEDICATIONS = [
        ("allergies", "Drug allergies or intolerances?"),
        ("medications", "Current medications (name, dose, frequency)?"),
        ("supplements", "Vitamins, supplements, or herbals?"),
    ]

    HISTORY = [
        ("previous_surgery", "Previous surgery on this joint?"),
        ("previous_problems", "Previous injuries or chronic pain in this area?"),
        ("autoimmune", "Autoimmune conditions (RA, lupus, etc.)?"),
    ]

    PAIN = [
        ("pain_location", "Where is your pain?"),
        ("pain_onset", "When did it start?"),
        ("pain_severity", "Pain severity (0-10 scale)?"),
        ("pain_quality", "Describe pain (sharp, dull, aching, throbbing)?"),
        ("pain_worse", "What makes it worse?"),
        ("pain_better", "What makes it better?"),
    ]

    FUNCTIONAL = [
        ("swelling", "Swelling, redness, warmth, or stiffness?"),
        ("movement", "Limitation in joint movements or daily activities?"),
        ("weakness", "Weakness in muscles or difficulty lifting?"),
    ]

    PHYSICAL_EXAM = [
        ("inspection", "Inspection findings (swelling, redness, deformity):"),
        ("palpation", "Palpation findings (tenderness, warmth, crepitus):"),
        ("range_of_motion", "Range of motion (active/passive, joints tested):"),
        ("strength", "Strength testing (0-5 grading, muscle groups):"),
        ("gait", "Gait observation (walking pattern, posture):"),
        ("special_tests", "Special tests performed (Lachman, McMurray, etc.):"),
    ]

    PATIENT_QUESTIONS = [
        ("diagnosis", "What exactly is wrong with me? What's causing my pain?"),
        ("timeline", "How long will recovery take?"),
        ("permanent", "Will this cause permanent damage or disability?"),
        ("treatment", "What are my treatment options?"),
        ("alternatives", "Are there natural or alternative treatments?"),
        ("activity", "What activities should I avoid?"),
        ("prevention", "How can I prevent this from happening again?"),
        ("lifestyle", "What lifestyle changes would help?"),
        ("complications", "What are potential complications?"),
        ("specialist", "Should I get a second opinion or see a specialist?"),
    ]


# ============================================================================
# CORE BUSINESS LOGIC
# ============================================================================

class ExamProcessor:
    """Core exam processing logic (UI-agnostic)."""

    @staticmethod
    def validate_answer(answer: str) -> str:
        """Validate and normalize answer."""
        return answer.strip() or "(no response)"

    @staticmethod
    def detect_red_flags(answers: Dict[str, str]) -> List[str]:
        """Detect red flags from answers."""
        flags = []

        if answers.get("fever", "").lower().startswith("y"):
            flags.append("Fever/night sweats reported")

        if answers.get("weight_loss", "").lower().startswith("y"):
            flags.append("Unexplained weight loss reported")

        if answers.get("neurologic", "").lower().startswith("y"):
            flags.append("Progressive neurological symptoms - requires urgent evaluation")

        if answers.get("bowel_bladder", "").lower().startswith("y"):
            flags.append("⚠️  CRITICAL: Bowel/bladder changes - Needs immediate physician evaluation")

        if answers.get("swelling_unilateral", "").lower().startswith("y"):
            flags.append("Unilateral swelling with calf pain - possible blood clot, needs evaluation")

        if answers.get("pain_rest", "").lower().startswith("y"):
            flags.append("Pain at rest unimproved - possible infection, needs evaluation")

        if answers.get("trauma_high", "").lower().startswith("y"):
            flags.append("High-energy trauma - fracture risk, imaging may be needed")

        if answers.get("systemic", "").lower().startswith("y"):
            flags.append("Systemic symptoms - may indicate rheumatologic disease")

        return flags

    @staticmethod
    def generate_assessment(
        answers: Dict[str, str],
        exam_findings: Dict[str, str]
    ) -> Assessment:
        """Generate clinical assessment from answers and exam findings."""

        all_answers = {**answers}
        red_flags = ExamProcessor.detect_red_flags(all_answers)

        urgency = "emergency" if any("CRITICAL" in f for f in red_flags) else \
                  "urgent" if len(red_flags) > 2 else \
                  "monitor" if red_flags else \
                  "normal"

        assessment = Assessment(
            red_flags=red_flags,
            primary_impression="Musculoskeletal examination findings documented. Further evaluation recommended.",
            urgency=urgency,
            recommendations=[
                "Physical therapy evaluation",
                "Activity modification as tolerated",
                "Follow-up assessment in 2 weeks",
            ]
        )

        return assessment

    @staticmethod
    def generate_education(assessment: Assessment) -> PatientEducation:
        """Generate patient education based on assessment."""

        education = PatientEducation(
            diagnosis="Based on exam findings. Your physician will provide specific diagnosis.",
            timeline="Recovery varies (typically 2-6 weeks). Your physician will give specific timeline.",
            permanent="Most musculoskeletal conditions are manageable. Permanent disability is rare with proper treatment.",
            treatment=f"Recommendations: {', '.join(assessment.recommendations)}",
            alternatives="Physical therapy is excellent. Discuss supplements with your physician.",
            activity="Avoid activities that significantly increase pain. Gradually return as tolerated.",
            prevention="Regular exercise, good posture, proper ergonomics, weight management.",
            lifestyle="Exercise regularly, sleep 7-9 hours, manage stress, eat anti-inflammatory foods.",
            complications="Rare with proper treatment. Your physician will monitor you.",
            specialist="Appropriate if symptoms don't improve in 4 weeks. Ask your physician for referral."
        )

        return education

    @staticmethod
    def create_exam_record(
        patient_name: str,
        exam_answers: ExamAnswers,
        physical_exam: PhysicalExam,
        assessment: Assessment,
        education: PatientEducation
    ) -> ExamRecord:
        """Create complete exam record."""

        record = ExamRecord(
            patient_name=patient_name,
            patient_id=f"MSK{datetime.now().strftime('%Y%m%d%H%M')}",
            encounter_id=f"ENC{datetime.now().strftime('%Y%m%d%H%M%S')}",
            timestamp=datetime.now(),
            answers=exam_answers,
            physical_exam=physical_exam,
            assessment=assessment,
            education=education
        )

        return record


# ============================================================================
# STATE MANAGEMENT
# ============================================================================

class ExamState:
    """Manages exam state throughout workflow."""

    def __init__(self):
        self.patient_name: Optional[str] = None
        self.red_flag_answers: Dict[str, str] = {}
        self.medication_answers: Dict[str, str] = {}
        self.history_answers: Dict[str, str] = {}
        self.pain_answers: Dict[str, str] = {}
        self.functional_answers: Dict[str, str] = {}
        self.physical_exam: Dict[str, str] = {}
        self.assessment: Optional[Assessment] = None
        self.education: Optional[PatientEducation] = None
        self.exam_record: Optional[ExamRecord] = None

    def set_patient_name(self, name: str):
        """Set patient name."""
        self.patient_name = name or "Unknown"

    def add_red_flag_answer(self, question_id: str, answer: str):
        """Add red flag answer."""
        self.red_flag_answers[question_id] = ExamProcessor.validate_answer(answer)

    def add_medication_answer(self, question_id: str, answer: str):
        """Add medication answer."""
        self.medication_answers[question_id] = ExamProcessor.validate_answer(answer)

    def add_history_answer(self, question_id: str, answer: str):
        """Add history answer."""
        self.history_answers[question_id] = ExamProcessor.validate_answer(answer)

    def add_pain_answer(self, question_id: str, answer: str):
        """Add pain answer."""
        self.pain_answers[question_id] = ExamProcessor.validate_answer(answer)

    def add_functional_answer(self, question_id: str, answer: str):
        """Add functional answer."""
        self.functional_answers[question_id] = ExamProcessor.validate_answer(answer)

    def add_exam_finding(self, field: str, value: str):
        """Add physical exam finding."""
        self.physical_exam[field] = ExamProcessor.validate_answer(value)

    def generate_assessment(self) -> Assessment:
        """Generate assessment from current answers."""
        all_answers = {
            **self.red_flag_answers,
            **self.medication_answers,
            **self.history_answers,
            **self.pain_answers,
            **self.functional_answers,
        }
        self.assessment = ExamProcessor.generate_assessment(all_answers, self.physical_exam)
        return self.assessment

    def generate_education(self) -> PatientEducation:
        """Generate education from assessment."""
        if not self.assessment:
            self.generate_assessment()

        self.education = ExamProcessor.generate_education(self.assessment)
        return self.education

    def finalize_exam(self) -> ExamRecord:
        """Create final exam record."""
        if not self.education:
            self.generate_education()

        exam_answers = ExamAnswers(
            red_flags=self.red_flag_answers,
            medications=self.medication_answers,
            history=self.history_answers,
            pain_assessment=self.pain_answers,
            functional=self.functional_answers,
        )

        physical_exam = PhysicalExam(
            inspection=self.physical_exam.get("inspection", ""),
            palpation=self.physical_exam.get("palpation", ""),
            range_of_motion=self.physical_exam.get("range_of_motion", ""),
            strength=self.physical_exam.get("strength", ""),
            gait=self.physical_exam.get("gait", ""),
            special_tests=self.physical_exam.get("special_tests", ""),
        )

        self.exam_record = ExamProcessor.create_exam_record(
            self.patient_name or "Unknown",
            exam_answers,
            physical_exam,
            self.assessment,
            self.education
        )

        return self.exam_record

    def to_dict(self) -> dict:
        """Export to dictionary."""
        if self.exam_record:
            return self.exam_record.model_dump(mode="json")
        return {}

    def reset(self):
        """Reset state for new exam."""
        self.__init__()


# ============================================================================
# EXPORT UTILITIES
# ============================================================================

class ExamExporter:
    """Export exam data in different formats."""

    @staticmethod
    def to_json(exam_record: ExamRecord) -> str:
        """Export to JSON string."""
        import json
        return json.dumps(exam_record.model_dump(mode="json"), indent=2, default=str)

    @staticmethod
    def to_dict(exam_record: ExamRecord) -> dict:
        """Export to dictionary."""
        return exam_record.model_dump(mode="json")

    @staticmethod
    def to_markdown(exam_record: ExamRecord) -> str:
        """Export to markdown."""
        md = f"""# Musculoskeletal Exam Report

**Patient:** {exam_record.patient_name}
**Patient ID:** {exam_record.patient_id}
**Encounter ID:** {exam_record.encounter_id}
**Date:** {exam_record.timestamp}

## Red Flags
{chr(10).join([f"- {flag}" for flag in exam_record.assessment.red_flags]) if exam_record.assessment.red_flags else "None detected"}

## Assessment
**Primary Impression:** {exam_record.assessment.primary_impression}
**Urgency:** {exam_record.assessment.urgency.upper()}

### Recommendations
{chr(10).join([f"- {rec}" for rec in exam_record.assessment.recommendations])}

## Patient Education

"""
        for q_id, question in QuestionSet.PATIENT_QUESTIONS:
            response = getattr(exam_record.education, q_id, "N/A")
            md += f"### {question}\n{response}\n\n"

        return md

    @staticmethod
    def save_json(exam_record: ExamRecord, filepath: str) -> str:
        """Save to JSON file."""
        save_model_response(exam_record, filepath)
        return filepath


# ============================================================================
# VALIDATION & CHECKS
# ============================================================================

class ExamValidator:
    """Validate exam completeness and quality."""

    @staticmethod
    def check_red_flags(assessment: Assessment) -> Tuple[bool, str]:
        """Check if critical red flags present."""
        critical = [f for f in assessment.red_flags if "CRITICAL" in f]
        if critical:
            return True, f"⚠️  CRITICAL: {critical[0]}"
        return False, ""

    @staticmethod
    def check_required_fields(state: ExamState) -> Tuple[bool, List[str]]:
        """Check if all required fields filled."""
        missing = []

        if not state.patient_name:
            missing.append("Patient name")
        if not state.red_flag_answers:
            missing.append("Red flag screening")
        if not state.physical_exam:
            missing.append("Physical examination")

        return len(missing) == 0, missing

    @staticmethod
    def get_completion_percentage(state: ExamState) -> int:
        """Get completion percentage."""
        total_questions = (
            len(QuestionSet.RED_FLAGS) +
            len(QuestionSet.MEDICATIONS) +
            len(QuestionSet.HISTORY) +
            len(QuestionSet.PAIN) +
            len(QuestionSet.FUNCTIONAL) +
            len(QuestionSet.PHYSICAL_EXAM)
        )

        answered = (
            len(state.red_flag_answers) +
            len(state.medication_answers) +
            len(state.history_answers) +
            len(state.pain_answers) +
            len(state.functional_answers) +
            len(state.physical_exam)
        )

        return int((answered / total_questions) * 100) if total_questions > 0 else 0
