from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

# ----------------------------
# 1. Pydantic Models
# ----------------------------
class PatientAnswer(BaseModel):
    question_id: str = Field(..., description="Unique identifier for patient question")
    question_text: str = Field(..., description="Text of the question asked to the patient")
    answer_text: str = Field(..., description="Patient's response")
    answer_code: Optional[str] = Field(None, description="Structured code representing answer type")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score for answer classification")

class NurseReport(BaseModel):
    inspection: dict = Field(..., description="Inspection findings of anus and rectum")
    digital_exam: dict = Field(..., description="Findings from digital rectal examination (DRE)")
    prostate_exam: dict = Field(..., description="Prostate size, consistency, nodules, tenderness")
    stool_sample: dict = Field(..., description="Stool characteristics, blood presence, sample id")
    media: Optional[dict] = Field(None, description="Optional media files: photos, videos")

class LLMAssessment(BaseModel):
    primary_impression: str = Field(..., description="Primary impression from LLM")
    urgency: Literal["normal", "monitor", "urgent", "emergency"] = Field(..., description="Triage urgency level")
    recommendations: List[str] = Field(..., description="Recommended clinical actions")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence of the assessment")

class ARPExam(BaseModel):
    patient_id: str = Field(..., description="Unique patient identifier")
    encounter_id: str = Field(..., description="Encounter unique identifier")
    timestamp: datetime = Field(..., description="Timestamp of exam")
    patient_answers: List[PatientAnswer] = Field(..., description="Patient history answers")
    nurse_report: NurseReport = Field(..., description="Structured nurse/proctor report")
    llm_assessment: LLMAssessment = Field(..., description="LLM assessment")

# ----------------------------
# 2. Patient questions
# ----------------------------
patient_questions = [
    ("q1_pain", "Do you have anal or rectal pain?"),
    ("q2_bleeding", "Any bleeding per rectum? Color, amount, frequency?"),
    ("q3_constipation", "Do you have constipation or difficulty passing stool?"),
    ("q4_diarrhea", "Do you have diarrhea or loose stools?"),
    ("q5_urinary", "Any urinary symptoms like difficulty, frequency, or pain?"),
    ("q6_prostate_symptoms", "Any sensation of incomplete bladder emptying, weak stream, nocturia?"),
    ("q7_family_history", "Any family history of colorectal or prostate disease?")
]

# ----------------------------
# 3. Nurse guidance with LLM help
# ----------------------------
nurse_fields = ["inspection", "digital_exam", "prostate_exam", "stool_sample", "media"]

nurse_help_prompts = {
    "inspection": "Inspect perianal region for lesions, hemorrhoids, skin tags, fissures. LLM help available if unsure.",
    "digital_exam": "Insert gloved lubricated finger to feel anal canal and rectum. Note sphincter tone, masses, tenderness.",
    "prostate_exam": "Palpate prostate for size, symmetry, consistency, nodules, tenderness.",
    "stool_sample": "Check for color, consistency, mucus, occult blood. Record sample ID.",
    "media": "Optional: Enter file paths for images or videos."
}

# ----------------------------
# 4. Mock LLM guidance
# ----------------------------
def ask_llm(question: str) -> str:
    guidance = {
        "digital": "Lubricate gloved finger, insert gently, feel rectal walls and sphincter tone.",
        "prostate": "Feel prostate size, shape, consistency, nodules; note tenderness.",
        "inspection": "Look for hemorrhoids, fissures, skin changes, masses.",
        "stool": "Describe color, consistency, presence of blood or mucus."
    }
    for key, resp in guidance.items():
        if key.lower() in question.lower():
            return resp
    return "Follow standard examination procedures carefully."

# ----------------------------
# 5. Interactive nurse report collection
# ----------------------------
def collect_nurse_report_arp():
    nurse_data = {}
    for field in nurse_fields:
        while True:
            print(f"\nEnter {field} findings. Type 'help' to ask LLM for guidance.")
            print(f"Hint: {nurse_help_prompts[field]}")
            response = input(f"{field}: ")
            if response.lower() == "help":
                question = input("Ask your question to LLM: ")
                llm_answer = ask_llm(question)
                print(f"LLM Guidance: {llm_answer}")
            else:
                nurse_data[field] = response
                break
    # Store as simple dicts/strings
    return NurseReport(
        inspection={"findings": nurse_data["inspection"]},
        digital_exam={"findings": nurse_data["digital_exam"]},
        prostate_exam={"findings": nurse_data["prostate_exam"]},
        stool_sample={"details": nurse_data["stool_sample"]},
        media=None if nurse_data["media"].strip() == "" else {"files": nurse_data["media"]}
    )

# ----------------------------
# 6. Collect patient answers
# ----------------------------
def collect_patient_answers_arp():
    answers = []
    for qid, qtext in patient_questions:
        ans_text = input(f"Patient - {qtext}: ")
        code = "none" if ans_text.lower() in ["no", "none"] else "present"
        answers.append(PatientAnswer(question_id=qid, question_text=qtext, answer_text=ans_text, answer_code=code, confidence=0.95))
    return answers

# ----------------------------
# 7. LLM Assessment simulation
# ----------------------------
def generate_llm_assessment_arp():
    return LLMAssessment(
        primary_impression="No obvious malignancy; consider hemorrhoids or prostatitis",
        urgency="monitor",
        recommendations=["Stool test if bleeding persists", "Consider DRE follow-up", "Monitor urinary symptoms"],
        confidence=0.9
    )

# ----------------------------
# 8. Main interactive function
# ----------------------------
def main_arp():
    print("=== Anus, Rectum, and Prostate Telemedicine Exam ===")
    patient_answers = collect_patient_answers_arp()
    print("\n--- Nurse measurements ---")
    nurse_report = collect_nurse_report_arp()
    llm_assessment = generate_llm_assessment_arp()

    exam = ARPExam(
        patient_id="P003",
        encounter_id="E20251023-ARP01",
        timestamp=datetime.now(),
        patient_answers=patient_answers,
        nurse_report=nurse_report,
        llm_assessment=llm_assessment
    )

    print("\n=== Structured ARPExam JSON ===")
    print(exam.model_dump_json(indent=4))

# ----------------------------
if __name__ == "__main__":
    main_arp()
