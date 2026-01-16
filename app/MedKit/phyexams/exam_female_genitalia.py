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
    inspection: dict = Field(..., description="Inspection of vulva, perineum, and surrounding areas")
    palpation: dict = Field(..., description="Palpation: vaginal walls, cervix, uterus, adnexa for masses, tenderness")
    speculum_exam: dict = Field(..., description="Speculum findings: cervix, discharge, lesions, bleeding")
    media: Optional[dict] = Field(None, description="Optional images or videos for telemedicine")

class LLMAssessment(BaseModel):
    primary_impression: str = Field(..., description="Primary impression from LLM")
    urgency: Literal["normal","monitor","urgent","emergency"] = Field(..., description="Triage urgency level")
    recommendations: List[str] = Field(..., description="Recommended clinical actions")
    confidence: Optional[float] = Field(None, description="Confidence of the assessment")

class FemaleGenitaliaExam(BaseModel):
    patient_id: str = Field(..., description="Patient unique identifier")
    encounter_id: str = Field(..., description="Encounter unique identifier")
    timestamp: datetime = Field(..., description="Timestamp of exam")
    patient_answers: List[PatientAnswer] = Field(..., description="Patient history responses")
    nurse_report: NurseReport = Field(..., description="Structured nurse report")
    llm_assessment: LLMAssessment = Field(..., description="LLM evaluation")

# ----------------------------
# 2. Patient questions
# ----------------------------
patient_questions = [
    ("q1_pain", "Any pain in vulva, vagina, or lower abdomen?"),
    ("q2_discharge", "Any abnormal vaginal discharge? Color, consistency, odor?"),
    ("q3_bleeding", "Any intermenstrual bleeding, post-coital bleeding, or heavy periods?"),
    ("q4_urinary", "Any urinary symptoms like burning, frequency, or urgency?"),
    ("q5_sexual", "Any sexual discomfort, pain with intercourse, or changes in libido?"),
    ("q6_trauma", "Any recent trauma or injury to genital area?"),
    ("q7_infection_history", "Any history of STIs, urinary, or gynecological infections?"),
    ("q8_menstrual_history", "Any irregularities in menstrual cycle or menopause?")
]

# ----------------------------
# 3. Mock LLM analysis function
# ----------------------------
def llm_analyze_answer(question: str, answer: str) -> dict:
    """
    Analyze patient answer and suggest follow-up questions.
    """
    if "yes" in answer.lower() or "pain" in answer.lower() or "discharge" in answer.lower():
        return {
            "answer_code": "present",
            "confidence": 0.95,
            "follow_up": [f"Please describe severity, duration, and location of {question.lower()}."]
        }
    elif "no" in answer.lower():
        return {"answer_code": "absent", "confidence": 0.98, "follow_up": None}
    else:
        return {"answer_code": "unclear", "confidence": 0.80, "follow_up": [f"Can you clarify your answer regarding {question.lower()}?"]}

# ----------------------------
# 4. Collect patient answers with dynamic follow-up
# ----------------------------
def collect_patient_answers_fge():
    answers = []
    for qid, qtext in patient_questions:
        ans_text = input(f"Patient - {qtext}: ")
        analysis = llm_analyze_answer(qtext, ans_text)
        pa = PatientAnswer(
            question_id=qid,
            question_text=qtext,
            answer_text=ans_text,
            answer_code=analysis["answer_code"],
            confidence=analysis["confidence"],
            follow_up=[]
        )
        # Ask follow-up questions if LLM suggests
        if analysis["follow_up"]:
            pa.follow_up = []
            for fq in analysis["follow_up"]:
                follow_up_answer = input(f"LLM Follow-up - {fq}: ")
                pa.follow_up.append(f"{fq} Answer: {follow_up_answer}")
        answers.append(pa)
    return answers

# ----------------------------
# 5. Nurse/examiner fields with LLM guidance
# ----------------------------
nurse_fields = ["inspection","palpation","speculum_exam","media"]
nurse_help_prompts = {
    "inspection": "Observe vulva, labia, clitoris, perineum for lesions, swelling, erythema.",
    "palpation": "Palpate vaginal walls, cervix, uterus, adnexa for masses, tenderness, nodules.",
    "speculum_exam": "Use speculum to visualize cervix, vaginal walls; check for discharge, bleeding, lesions.",
    "media": "Optional: provide images or video (lesion photo, ultrasound)."
}

def ask_llm(question: str) -> str:
    guidance = {
        "inspection": "Look for swelling, redness, lesions, discharge, or signs of infection.",
        "palpation": "Gently palpate cervix, uterus, adnexa; note tenderness or masses.",
        "speculum": "Visualize cervix and vaginal walls; note discharge, bleeding, or lesions."
    }
    for key, resp in guidance.items():
        if key in question.lower():
            return resp
    return "Follow standard gynecological examination procedures."

def collect_nurse_report_fge():
    nurse_data = {}
    for field in nurse_fields:
        while True:
            print(f"\nEnter {field} findings. Type 'help' to ask LLM for guidance.")
            print(f"Hint: {nurse_help_prompts[field]}")
            response = input(f"{field}: ")
            if response.lower() == "help":
                question = input("Ask your question to LLM: ")
                print(f"LLM Guidance: {ask_llm(question)}")
            else:
                nurse_data[field] = response
                break
    return NurseReport(
        inspection={"findings": nurse_data["inspection"]},
        palpation={"findings": nurse_data["palpation"]},
        speculum_exam={"findings": nurse_data["speculum_exam"]},
        media=None if nurse_data["media"].strip()==""else {"files": nurse_data["media"]}
    )

# ----------------------------
# 6. LLM assessment simulation
# ----------------------------
def generate_llm_assessment_fge():
    return LLMAssessment(
        primary_impression="No suspicious lesion; mild vaginal discharge, likely infectious",
        urgency="monitor",
        recommendations=["Consider vaginal swab for culture","Symptomatic treatment for infection","Follow-up in 1 week"],
        confidence=0.9
    )

# ----------------------------
# 7. Main interactive FGE
# ----------------------------
def main_fge():
    print("=== Female Genitalia Telemedicine Exam ===")
    patient_answers = collect_patient_answers_fge()
    print("\n--- Nurse / Examiner Inputs ---")
    nurse_report = collect_nurse_report_fge()
    llm_assessment = generate_llm_assessment_fge()

    exam = FemaleGenitaliaExam(
        patient_id="F100",
        encounter_id="E20251023-FGE01",
        timestamp=datetime.now(),
        patient_answers=patient_answers,
        nurse_report=nurse_report,
        llm_assessment=llm_assessment
    )

    print("\n=== Structured FemaleGenitaliaExam JSON ===")
    print(exam.model_dump_json(indent=4))

if __name__ == "__main__":
    main_fge()
