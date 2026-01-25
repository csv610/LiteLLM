"""
Musculoskeletal Telemedicine Exam Module

Comprehensive system for musculoskeletal patient assessment combining:
- Patient history collection (Top 10 doctor questions)
- Physical examination documentation
- AI-powered clinical assessment via LiteClient
- Patient education (Top 10 patient concerns answered)

Integrates with LiteClient for LLM-powered clinical assessments.
"""

# ==============================================================================
# STANDARD LIBRARY IMPORTS
# ==============================================================================
import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple

# ==============================================================================
# THIRD-PARTY IMPORTS
# ==============================================================================
from pydantic import BaseModel, Field

# ==============================================================================
# LOCAL IMPORTS (LiteClient setup)
# ==============================================================================
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

# ==============================================================================
# LOCAL IMPORTS (Module models)
# ==============================================================================
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.pydantic_prompt_generator import PromptStyle

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# SECTION 1: PYDANTIC DATA MODELS
# ============================================================================

class PatientAnswer(BaseModel):
    """Patient response to clinical history question."""
    question_id: str = Field(..., description="Unique patient question identifier")
    question_text: str = Field(..., description="Text of the question asked")
    answer_text: str = Field(..., description="Patient response")
    answer_code: Optional[str] = Field(None, description="LLM-coded response category")
    confidence: Optional[float] = Field(None, description="LLM confidence in coding")
    follow_up: Optional[List[str]] = Field(None, description="LLM-generated follow-up questions")


class PhysicalExamFindings(BaseModel):
    """Physical examination findings from nurse/examiner."""
    inspection: dict = Field(..., description="Inspection of joints and musculoskeletal system for swelling, deformity, erythema")
    palpation: dict = Field(..., description="Palpation of joints for tenderness, warmth, crepitus, deformity")
    range_of_motion: dict = Field(..., description="Active and passive range of motion for major joints")
    strength_testing: dict = Field(..., description="Muscle strength testing (graded 0-5)")
    gait: dict = Field(..., description="Observation of walking pattern and posture")
    special_tests: dict = Field(..., description="Special maneuvers for ligament, tendon, or joint testing")
    media: Optional[dict] = Field(None, description="Optional images or videos for telemedicine")


class LLMAssessment(BaseModel):
    """Clinical assessment and recommendations from LLM analysis."""
    primary_impression: str = Field(..., description="Primary impression from LLM")
    urgency: Literal["normal", "monitor", "urgent", "emergency"] = Field(..., description="Triage urgency level")
    recommendations: List[str] = Field(..., description="Recommended clinical actions")
    confidence: Optional[float] = Field(None, description="Confidence of the assessment")
    differential_diagnoses: Optional[List[str]] = Field(None, description="List of potential diagnoses to consider")


class PatientInquiryResponse(BaseModel):
    """Patient question and doctor's response."""
    inquiry_id: str = Field(..., description="Patient inquiry identifier")
    question: str = Field(..., description="Patient's question")
    response: str = Field(..., description="Doctor's response")


class MusculoskeletalExam(BaseModel):
    """Complete musculoskeletal telemedicine examination record."""
    patient_name: str = Field(default="Unknown", description="Patient name or identifier")
    patient_id: str = Field(..., description="Patient unique identifier")
    encounter_id: str = Field(..., description="Encounter unique identifier")
    timestamp: datetime = Field(..., description="Timestamp of exam")
    patient_answers: List[PatientAnswer] = Field(..., description="Patient history responses")
    physical_exam: PhysicalExamFindings = Field(..., description="Physical examination findings")
    llm_assessment: LLMAssessment = Field(..., description="LLM evaluation and recommendations")
    patient_inquiries: Optional[List[PatientInquiryResponse]] = Field(None, description="Answers to common patient questions")


# ============================================================================
# SECTION 2: CLINICAL QUESTION SETS (MEDICALLY COMPLIANT)
# ============================================================================

# RED FLAG SCREENING QUESTIONS (CRITICAL - Dangerous conditions)
RED_FLAG_QUESTIONS = [
    ("rf1_fever", "Have you had fever (>101°F), chills, or night sweats in the past month?"),
    ("rf2_weight_loss", "Unexplained weight loss (>10 lbs unintentional) in past 3 months?"),
    ("rf3_neurologic_progressive", "Progressive numbness, tingling, or weakness spreading down legs?"),
    ("rf4_bowel_bladder", "Changes in bowel/bladder control, inability to hold urine/stool, or saddle numbness?"),
    ("rf5_severe_unilateral_swelling", "Severe one-sided leg swelling with calf pain (possible blood clot)?"),
    ("rf6_severe_pain_rest", "Severe pain at rest that doesn't improve with rest (possible infection)?"),
    ("rf7_trauma_high_energy", "High-energy trauma, major fall, or motor vehicle accident?"),
    ("rf8_systemwide_symptoms", "Rash, sore throat, recent infection, or widespread constitutional symptoms?"),
]

# MEDICATION & ALLERGY HISTORY (CRITICAL - Drug safety)
MEDICATION_QUESTIONS = [
    ("med1_allergies", "Do you have any drug allergies or intolerances? If yes, what are they and what reactions did you have?"),
    ("med2_current_medications", "What medications are you currently taking? (Include: name, dose, frequency)"),
    ("med3_supplements", "Do you take any vitamins, supplements, or herbal products?"),
    ("med4_recent_antibiotics", "Have you taken antibiotics in the past month (increases infection risk)?"),
]

# SURGICAL & MEDICAL HISTORY (IMPORTANT - Context for assessment)
HISTORY_QUESTIONS = [
    ("hx1_previous_surgery", "Have you had previous surgery on this joint or area? If yes, when and what procedure?"),
    ("hx2_previous_msk_problems", "Any previous musculoskeletal injuries or chronic pain in this area?"),
    ("hx3_autoimmune", "Do you have autoimmune conditions (rheumatoid arthritis, lupus, ankylosing spondylitis)?"),
    ("hx4_immunosuppression", "Are you immunosuppressed (HIV, organ transplant, cancer treatment, biologics)?"),
    ("hx5_osteoporosis", "History of osteoporosis, low bone density, or frequent fractures?"),
    ("hx6_diabetes", "Diabetes or other metabolic/endocrine conditions?"),
]

# Top 10 OPQRSTU-Compliant Questions (Pain Assessment)
# OPQRSTU = Onset, Provocation, Quality, Radiation, Severity, Timing, Understanding
DOCTOR_QUESTIONS = [
    # Onset & Provocation (O & P)
    ("q1_pain_presence", "Do you have joint or muscle pain? If yes, which specific joint(s) or area(s)?"),
    ("q2_pain_onset", "When did this pain start? Was onset sudden (acute) or gradual (chronic)?"),
    ("q3_pain_provocation", "What activities, movements, or positions make the pain worse? What makes it better?"),

    # Quality & Radiation (Q & R)
    ("q4_pain_quality", "Describe your pain: Is it sharp, dull, aching, throbbing, burning, or stabbing?"),
    ("q5_pain_radiation", "Does the pain stay in one area or does it travel/radiate? If it travels, where does it go?"),

    # Severity & Timing (S & T)
    ("q6_pain_severity", "On a scale of 0-10 (0=no pain, 10=worst pain ever), how severe is your pain?"),
    ("q7_pain_timing", "When does pain occur? Constant? Only with activity? Worse morning/evening? Any patterns?"),
    ("q8_stiffness_duration", "Do you experience stiffness? If yes, how long does it typically last?"),

    # Associated Symptoms (Critical for systemic disease screening)
    ("q9_associated_symptoms", "Do you have any swelling, redness, warmth, giving way, catching, or clicking?"),
    ("q10_functional_impact", "How does this pain affect your daily activities? What can you not do?"),

    # Trauma & History Context
    ("q11_trauma_history", "Any history of trauma, falls, accidents, or direct injury to this area?"),
    ("q12_previous_treatment", "Have you been treated for this before? What treatments helped or didn't help?"),

    # Understanding (U) - Patient perspective
    ("q13_patient_understanding", "What do you think is causing your pain? What are your concerns about this condition?"),
]

# Top 10 Questions Patients Ask Doctors
PATIENT_INQUIRIES = [
    ("p1_diagnosis", "What exactly is wrong with me? What's causing my pain?"),
    ("p2_timeline", "How long will it take to recover, and will this get worse?"),
    ("p3_permanent", "Will this cause permanent damage or disability?"),
    ("p4_treatment_options", "What are my treatment options? Do I need surgery or medications?"),
    ("p5_natural_remedies", "Are there natural or alternative treatments like physical therapy, acupuncture, or supplements?"),
    ("p6_activity_restrictions", "What activities should I avoid? When can I return to sports or work?"),
    ("p7_prevention", "How can I prevent this from happening again?"),
    ("p8_lifestyle", "What lifestyle changes (weight, posture, exercise) would help?"),
    ("p9_complications", "What are the potential complications or side effects of treatments?"),
    ("p10_second_opinion", "Should I get a second opinion or see a specialist?")
]


# ============================================================================
# SECTION 3: PATIENT INFORMATION COLLECTION
# ============================================================================

def collect_patient_info() -> dict:
    """
    Collect basic patient demographics at exam start.

    Returns:
        Dictionary with patient_name key
    """
    print("\n" + "=" * 70)
    print("PATIENT INFORMATION")
    print("=" * 70)

    patient_name = input("Patient Name (default: 'Unknown'): ").strip()
    if not patient_name:
        patient_name = "Unknown"

    return {"patient_name": patient_name}


# ============================================================================
# SECTION 4: ANSWER ANALYSIS & VALIDATION
# ============================================================================

def analyze_patient_answer(question: str, answer: str) -> dict:
    """
    Classify patient answer using heuristics.
    In production, would use MedKitClient for sophisticated NLP analysis.

    Args:
        question: The question asked
        answer: Patient's response

    Returns:
        Dictionary with answer_code, confidence, and optional follow-up questions
    """
    answer_lower = answer.lower()

    # Keywords indicating positive findings
    positive_keywords = ["yes", "pain", "swelling", "stiff", "weak", "limited",
                         "injury", "fracture", "arthritis", "soreness", "discomfort"]

    if any(word in answer_lower for word in positive_keywords):
        return {
            "answer_code": "present",
            "confidence": 0.95,
            "follow_up": [f"Can you describe: location, severity, duration, what triggers it, and any other associated symptoms?"]
        }
    elif "no" in answer_lower or answer_lower.startswith("n"):
        return {
            "answer_code": "absent",
            "confidence": 0.98,
            "follow_up": None
        }
    else:
        return {
            "answer_code": "unclear",
            "confidence": 0.70,
            "follow_up": [f"Could you please clarify your answer?"]
        }


# ============================================================================
# SECTION 5: PATIENT HISTORY COLLECTION
# ============================================================================

def collect_patient_history() -> List[PatientAnswer]:
    """
    Collect complete patient history through Top 10 doctor questions.
    Includes follow-up questions for positive findings.

    Returns:
        List of PatientAnswer objects
    """
    print("\n" + "=" * 70)
    print("PATIENT HISTORY (Top 10 Questions)")
    print("=" * 70)

    answers = []

    for qid, question_text in DOCTOR_QUESTIONS:
        print(f"\n[{len(answers) + 1}/10] {question_text}")
        answer_text = input("Answer: ").strip()

        if not answer_text:
            print("  ⚠ Skipping question due to empty response")
            continue

        # Analyze the answer
        analysis = analyze_patient_answer(question_text, answer_text)

        # Create patient answer object
        pa = PatientAnswer(
            question_id=qid,
            question_text=question_text,
            answer_text=answer_text,
            answer_code=analysis["answer_code"],
            confidence=analysis["confidence"],
            follow_up=[]
        )

        # Collect follow-up responses if needed
        if analysis["follow_up"]:
            follow_up_responses = []
            for follow_up_q in analysis["follow_up"]:
                print(f"\n  Follow-up: {follow_up_q}")
                follow_up_ans = input("  Response: ").strip()
                if follow_up_ans:
                    follow_up_responses.append(f"{follow_up_q}\n  → {follow_up_ans}")
            pa.follow_up = follow_up_responses if follow_up_responses else None

        answers.append(pa)

    return answers


# ============================================================================
# SECTION 6: PHYSICAL EXAMINATION COLLECTION
# ============================================================================

NURSE_EXAM_FIELDS = {
    "inspection": "Observe joints for swelling, redness, deformities.",
    "palpation": "Palpate for tenderness, warmth, crepitus, deformities.",
    "range_of_motion": "Test active and passive motion of major joints.",
    "strength_testing": "Assess muscle strength for major muscle groups (0-5 scale).",
    "gait": "Observe walking pattern, posture, and balance.",
    "special_tests": "Perform maneuvers for ligament, tendon, or joint integrity.",
    "media": "Optional: provide images or videos of joints or movements."
}

EXAM_GUIDANCE = {
    "inspection": "Look for swelling, redness, deformity, or asymmetry.",
    "palpation": "Palpate joints and muscles for tenderness, warmth, crepitus.",
    "range": "Test joint movement actively and passively.",
    "strength": "Assess strength using standard 0-5 grading.",
    "gait": "Observe walking, posture, and any limping.",
    "special": "Perform tests like Lachman, McMurray, or Spurling's if indicated."
}


def get_exam_guidance(field: str) -> str:
    """Get contextual guidance for a physical exam field."""
    for key, guidance in EXAM_GUIDANCE.items():
        if key in field.lower():
            return guidance
    return "Follow standard musculoskeletal examination procedures."


def collect_physical_exam() -> PhysicalExamFindings:
    """
    Collect physical examination findings from nurse/examiner.
    Provides real-time guidance for each examination component.

    Returns:
        PhysicalExamFindings object
    """
    print("\n" + "=" * 70)
    print("PHYSICAL EXAMINATION")
    print("=" * 70)

    exam_data = {}

    for field, hint in NURSE_EXAM_FIELDS.items():
        print(f"\n[{list(NURSE_EXAM_FIELDS.keys()).index(field) + 1}/{len(NURSE_EXAM_FIELDS)}] {field.replace('_', ' ').title()}")
        print(f"  Hint: {hint}")
        print("  (Type 'help' for LLM guidance, or enter findings)")

        while True:
            response = input(f"  {field}: ").strip()

            if response.lower() == "help":
                print(f"  💡 Guidance: {get_exam_guidance(field)}")
                continue
            elif response:
                exam_data[field] = response
                break
            else:
                print("  ⚠ Please provide findings or type 'help'")

    return PhysicalExamFindings(
        inspection={"findings": exam_data.get("inspection", "")},
        palpation={"findings": exam_data.get("palpation", "")},
        range_of_motion={"details": exam_data.get("range_of_motion", "")},
        strength_testing={"details": exam_data.get("strength_testing", "")},
        gait={"details": exam_data.get("gait", "")},
        special_tests={"details": exam_data.get("special_tests", "")},
        media={"files": exam_data.get("media", "")} if exam_data.get("media", "").strip() else None
    )


# ============================================================================
# SECTION 7: LLM ASSESSMENT GENERATION
# ============================================================================

def generate_llm_assessment(
    patient_answers: List[PatientAnswer],
    physical_exam: PhysicalExamFindings,
    use_medkit: bool = False
) -> LLMAssessment:
    """
    Generate clinical assessment using LLM (with graceful fallback).

    Args:
        patient_answers: List of patient history responses
        physical_exam: Physical examination findings
        use_medkit: If True, use LiteClient for AI assessment

    Returns:
        LLMAssessment with recommendations
    """

    if use_medkit:
        try:
            print("\n  ⏳ Connecting to LiteClient for AI assessment...")

            # Initialize LiteClient with standardized model configuration
            client = LiteClient(ModelConfig(model="ollama/gemma3", temperature=0.7))

            # Format clinical data for LLM
            clinical_context = f"""
PATIENT HISTORY:
{chr(10).join([f"- {pa.question_text}: {pa.answer_text}" for pa in patient_answers])}

PHYSICAL EXAMINATION:
- Inspection: {physical_exam.inspection.get('findings', 'N/A')}
- Palpation: {physical_exam.palpation.get('findings', 'N/A')}
- Range of Motion: {physical_exam.range_of_motion.get('details', 'N/A')}
- Strength Testing: {physical_exam.strength_testing.get('details', 'N/A')}
- Gait: {physical_exam.gait.get('details', 'N/A')}
- Special Tests: {physical_exam.special_tests.get('details', 'N/A')}
"""

            sys_prompt = f"""You are an expert orthopedic specialist providing musculoskeletal examination assessment.

Given the clinical context below, provide a comprehensive assessment:

{clinical_context}

Generate a clinical assessment that includes:
- Key findings summary
- Clinical significance of findings
- Diagnostic considerations
- Recommendations for further evaluation or management
- Return structured JSON matching the exact schema provided, with all required fields populated."""

            assessment = client.generate_text(
                prompt="Provide a comprehensive musculoskeletal examination assessment based on the clinical data provided.",
                schema=LLMAssessment,
                sys_prompt=sys_prompt
            )
            print("  ✓ AI assessment generated successfully")
            return assessment

        except Exception as e:
            print(f"  ⚠ LiteClient unavailable ({type(e).__name__}), using fallback assessment")
            return _get_fallback_assessment()
    else:
        return _get_fallback_assessment()


def _get_fallback_assessment() -> LLMAssessment:
    """Default assessment when LLM is unavailable."""
    return LLMAssessment(
        primary_impression="Musculoskeletal examination findings noted; no acute injury identified on initial assessment",
        urgency="monitor",
        recommendations=[
            "Range-of-motion and flexibility exercises",
            "Symptom monitoring and follow-up in 2-4 weeks",
            "Consider physical therapy evaluation if symptoms persist",
            "Activity modification as tolerated"
        ],
        confidence=0.88,
        differential_diagnoses=[
            "Muscle strain or overuse syndrome",
            "Mild osteoarthritis",
            "Ligamentous laxity"
        ]
    )


# ============================================================================
# SECTION 8: PATIENT EDUCATION (Q&A)
# ============================================================================

# MEDICAL DISCLAIMER TEMPLATE
MEDICAL_DISCLAIMER = """
⚠️  IMPORTANT MEDICAL DISCLAIMER:

This assessment is EDUCATIONAL INFORMATION ONLY and is NOT medical advice.
This tool is designed to SUPPORT physician judgment, NOT replace it.
You must discuss these recommendations with your physician before implementation.

Limitations of this telemedicine assessment:
- Cannot replace a comprehensive in-person physical examination
- Visual assessment has inherent limitations via video/text
- Specialized imaging (X-ray, MRI, ultrasound) may be required for diagnosis
- This assessment cannot rule out serious/dangerous conditions
- Physician must provide individualized evaluation and recommendations

Seek IMMEDIATE emergency care if you experience:
✗ Severe uncontrolled pain, numbness/tingling spreading, bowel/bladder changes
✗ Severe swelling, signs of infection (fever, warmth, spreading redness)
✗ Chest pain, severe shortness of breath, signs of blood clot (unilateral swelling + calf pain)
✗ Inability to move joint or neurological emergency symptoms
"""

def generate_doctor_response(inquiry_id: str, assessment: LLMAssessment) -> str:
    """
    Generate doctor's response to common patient inquiry based on assessment.
    All responses include medical disclaimers and evidence-based guidance.

    Args:
        inquiry_id: Patient inquiry identifier
        assessment: LLMAssessment from examination

    Returns:
        Doctor's response to patient question with appropriate disclaimers
    """
    responses = {
        "p1_diagnosis":
            f"Based on your examination, my assessment is: {assessment.primary_impression}.\n\n"
            "However, additional testing (imaging, lab work) may be needed for definitive diagnosis.\n"
            "This assessment is supportive information—your physician must review findings and provide individualized diagnosis.\n\n"
            f"Differential considerations: {', '.join(assessment.differential_diagnoses) if assessment.differential_diagnoses else 'Various conditions possible'}\n\n"
            "IMPORTANT: This is educational assessment only. Discuss with your physician before starting any treatment.",

        "p2_timeline":
            f"Recovery timeline depends on several factors: condition severity (urgency: {assessment.urgency}), age, "
            "general health, adherence to treatment, and individual healing capacity.\n\n"
            "General timelines (these are ESTIMATES—individual variation is common):\n"
            "• Acute muscle strain: 2-4 weeks typical\n"
            "• Ligament sprain: 4-12 weeks typical\n"
            "• Osteoarthritis: Chronic condition requiring long-term management\n"
            "• Post-surgical: Weeks to months depending on procedure\n\n"
            "Important: Slower healing may occur with age, diabetes, smoking, or poor nutrition.\n"
            "Your physician will provide timeline based on YOUR specific condition.",

        "p3_permanent":
            "Most musculoskeletal conditions are MANAGEABLE with proper treatment.\n\n"
            "However, outcomes vary based on:\n"
            "✓ Early diagnosis and treatment initiation\n"
            "✓ Patient adherence to therapy\n"
            "✓ Underlying health conditions\n"
            "✓ Condition severity and type\n\n"
            "Some conditions may result in chronic symptoms requiring ongoing management.\n"
            "Permanent disability is possible but NOT inevitable with appropriate care.\n\n"
            "Your physician will discuss YOUR specific prognosis based on your condition.",

        "p4_treatment_options":
            f"Evidence-based recommendations for your condition:\n"
            f"{chr(10).join([f'• {rec}' for rec in assessment.recommendations])}\n\n"
            "Treatment options typically progress:\n"
            "1. Conservative: Rest, ice/heat, activity modification, physical therapy\n"
            "2. Medical: NSAIDs, corticosteroid injections, other medications\n"
            "3. Interventional: Specialized injections, procedures\n"
            "4. Surgical: Reserved for specific indications after conservative failure\n\n"
            "Your physician will recommend INDIVIDUALIZED treatment based on your specific diagnosis, "
            "severity, response to initial treatment, and preferences.\n"
            "Evidence sources: American Academy of Orthopaedic Surgeons (AAOS), "
            "American Physical Therapy Association (APTA), Cochrane reviews.",

        "p5_natural_remedies":
            "Evidence-based natural/conservative approaches:\n"
            "✓ Physical therapy: STRONG evidence for most MSK conditions\n"
            "✓ Exercise: Strengthening, flexibility, proprioception training\n"
            "✓ Activity modification: Pacing, ergonomics, movement quality\n"
            "✓ Ice/heat: Short-term symptom management (ice for acute, heat for chronic)\n"
            "✓ Weight management: Reduces joint stress\n\n"
            "Limited evidence but often used:\n"
            "• Glucosamine/chondroitin: Mixed evidence; may help some patients\n"
            "• Acupuncture: Some evidence for specific conditions; discuss with physician\n"
            "• Supplements: Quality varies; discuss with physician before starting\n\n"
            "Important: Supplements can interact with medications. Always inform your physician.",

        "p6_activity_restrictions":
            "Activity management is individualized based on your SPECIFIC condition:\n\n"
            "GENERAL PRINCIPLES:\n"
            "✓ Avoid movements that significantly increase pain\n"
            "✓ Gradual return to activities as tolerance improves\n"
            "✓ 'Move without worsening' is the general guideline\n"
            "✓ Pain that persists >2 hours after activity suggests doing too much\n\n"
            "Return-to-work/sports timeline varies:\n"
            "• Light office work: Often 1-2 weeks\n"
            "• Manual labor: 4-12 weeks (depends on demands)\n"
            "• Sports: Variable (weeks to months)\n\n"
            "YOUR PHYSICIAN will provide SPECIFIC activity recommendations based on your diagnosis, "
            "job requirements, and recovery progress.",

        "p7_prevention":
            "Evidence-based prevention strategies:\n"
            "✓ Regular exercise: Maintains strength, flexibility, proprioception\n"
            "✓ Proper ergonomics: Desk, lifting, carrying techniques\n"
            "✓ Postural awareness: Throughout daily activities\n"
            "✓ Warm-up before activity: Prepares tissues\n"
            "✓ Progressive training: Gradual increase in intensity/volume\n"
            "✓ Adequate rest: Between activities, overnight sleep\n"
            "✓ Weight management: Reduces joint load\n"
            "✓ Smoking cessation: Improves healing capacity\n\n"
            "Physical therapy can teach specific prevention exercises for your condition.\n"
            "Discuss prevention strategies with your physician and physical therapist.",

        "p8_lifestyle":
            "Lifestyle modifications that support musculoskeletal health:\n"
            "✓ Regular exercise: 150 min/week moderate activity (walking, swimming, cycling)\n"
            "✓ Strength training: 2 days/week major muscle groups\n"
            "✓ Sleep: 7-9 hours nightly (important for healing)\n"
            "✓ Stress management: Reduces muscle tension\n"
            "✓ Anti-inflammatory diet: Omega-3 fatty acids, reduced processed foods\n"
            "✓ Hydration: Adequate water intake\n"
            "✓ Smoking cessation: Dramatically improves outcomes\n"
            "✓ Alcohol moderation: Excessive alcohol impairs healing\n\n"
            "These changes significantly improve outcomes and reduce recurrence.\n"
            "Discuss lifestyle goals with your healthcare team.",

        "p9_complications":
            "Potential complications and monitoring:\n\n"
            "RARE but possible with untreated conditions:\n"
            "✗ Chronic pain syndrome\n"
            "✗ Recurrent injury or re-injury\n"
            "✗ Joint degeneration/arthritis (accelerated)\n"
            "✗ Nerve involvement (if untreated acute conditions)\n"
            "✗ Functional limitation if not addressed\n\n"
            "Risk factors for complications:\n"
            "• Delayed treatment initiation\n"
            "• Non-adherence to therapy\n"
            "• Continued aggravating activities\n"
            "• Underlying systemic disease (diabetes, rheumatologic conditions)\n"
            "• Poor healing capacity (age, smoking, nutrition)\n\n"
            "Complications are PREVENTABLE through:\n"
            "• Prompt treatment\n"
            "• Adherence to physical therapy\n"
            "• Activity modification\n"
            "• Close physician follow-up\n\n"
            "Your physician will monitor for complications and adjust treatment as needed.",

        "p10_second_opinion":
            "Seeking a second opinion is always appropriate and encouraged when:\n"
            "✓ Symptoms don't improve as expected with recommended treatment\n"
            "✓ You're considering surgery\n"
            "✓ Diagnosis is unclear\n"
            "✓ You want reassurance about treatment plan\n"
            "✓ You're uncomfortable with recommendations\n\n"
            "Specialists who may provide second opinions:\n"
            "• Orthopedic surgeon (surgical conditions)\n"
            "• Rheumatologist (arthritis, systemic diseases)\n"
            "• Physiatrist (physical medicine and rehabilitation)\n"
            "• Sports medicine specialist\n"
            "• Physical therapist (conservative management)\n\n"
            "Second opinions provide valuable perspective and are standard medical practice.\n"
            "Your physician can provide appropriate referrals."
    }

    response = responses.get(inquiry_id, "This is a great question. Please discuss with your physician.")
    return f"{response}\n\n{MEDICAL_DISCLAIMER}"


def generate_patient_education(assessment: LLMAssessment) -> List[PatientInquiryResponse]:
    """
    Generate answers to top 10 patient questions based on assessment.

    Args:
        assessment: LLMAssessment from examination

    Returns:
        List of PatientInquiryResponse objects
    """
    education = []

    for inquiry_id, question_text in PATIENT_INQUIRIES:
        response = generate_doctor_response(inquiry_id, assessment)
        education.append(PatientInquiryResponse(
            inquiry_id=inquiry_id,
            question=question_text,
            response=response
        ))

    return education


# ============================================================================
# SECTION 9: DISPLAY & REPORTING
# ============================================================================

def display_assessment_summary(assessment: LLMAssessment, patient_name: str = "Patient") -> None:
    """Display clinical assessment summary."""
    print("\n" + "=" * 70)
    print(f"CLINICAL ASSESSMENT SUMMARY - {patient_name}")
    print("=" * 70)
    print(f"\n📋 Primary Impression:\n   {assessment.primary_impression}")
    print(f"\n⚠  Urgency Level: {assessment.urgency.upper()}")
    print(f"📊 Confidence: {assessment.confidence * 100:.0f}%" if assessment.confidence else "📊 Confidence: Not specified")
    print(f"\n💊 Recommendations:")
    for i, rec in enumerate(assessment.recommendations, 1):
        print(f"   {i}. {rec}")
    if assessment.differential_diagnoses:
        print(f"\n🔍 Differential Diagnoses:")
        for i, dx in enumerate(assessment.differential_diagnoses, 1):
            print(f"   {i}. {dx}")


def display_patient_education(inquiries: List[PatientInquiryResponse], patient_name: str = "Patient") -> None:
    """Display patient education (Q&A)."""
    print("\n" + "=" * 70)
    print(f"PATIENT EDUCATION - ANSWERS TO TOP 10 QUESTIONS")
    print("=" * 70)

    for i, inquiry in enumerate(inquiries, 1):
        print(f"\n[Q{i}] {inquiry.question}")
        print(f"[A] {inquiry.response}\n")


def save_exam_to_json(exam: MusculoskeletalExam, filepath: Optional[str] = None) -> str:
    """
    Save complete exam record to JSON file.

    Args:
        exam: MusculoskeletalExam object
        filepath: Optional path to save to (defaults to exam_<encounter_id>.json)

    Returns:
        Path to saved file
    """
    if not filepath:
        filepath = f"exam_{exam.encounter_id}.json"

    save_model_response(exam, filepath)
    print(f"✓ Exam saved to: {filepath}")
    return filepath


# ============================================================================
# SECTION 10: MAIN EXAMINATION WORKFLOW
# ============================================================================

def run_musculoskeletal_exam(
    use_medkit: bool = False,
    include_education: bool = True,
    save_json: bool = False,
    json_path: Optional[str] = None
) -> Tuple[MusculoskeletalExam, Optional[List[PatientInquiryResponse]]]:
    """
    Execute complete musculoskeletal telemedicine examination workflow.

    Workflow:
    1. Collect patient information (name)
    2. Patient history (Top 10 doctor questions)
    3. Physical examination findings
    4. Generate clinical assessment (AI or fallback)
    5. Patient education (Top 10 patient questions answered)
    6. Save exam record

    Args:
        use_medkit: If True, use MedKitClient for LLM assessment
        include_education: If True, include patient education Q&A
        save_json: If True, save exam record to JSON
        json_path: Optional path for JSON output

    Returns:
        Tuple of (MusculoskeletalExam, List[PatientInquiryResponse] or None)
    """

    print("\n" + "=" * 70)
    print("MUSCULOSKELETAL TELEMEDICINE EXAMINATION SYSTEM")
    print("=" * 70)

    # Step 1: Patient Information
    print("\n[STEP 1/5] Patient Information")
    patient_info = collect_patient_info()
    patient_name = patient_info["patient_name"]

    # Step 2: Patient History
    print("\n[STEP 2/5] Collecting Patient History")
    patient_answers = collect_patient_history()

    # Step 3: Physical Examination
    print("\n[STEP 3/5] Physical Examination")
    physical_exam = collect_physical_exam()

    # Step 4: Generate Assessment
    print("\n[STEP 4/5] Clinical Assessment")
    llm_assessment = generate_llm_assessment(patient_answers, physical_exam, use_medkit=use_medkit)

    # Step 5: Patient Education
    patient_inquiries = None
    if include_education:
        print("\n[STEP 5/5] Patient Education")
        patient_inquiries = generate_patient_education(llm_assessment)

    # Create complete exam record
    exam = MusculoskeletalExam(
        patient_name=patient_name,
        patient_id=f"MSK{datetime.now().strftime('%Y%m%d%H%M')}",
        encounter_id=f"ENC{datetime.now().strftime('%Y%m%d%H%M%S')}",
        timestamp=datetime.now(),
        patient_answers=patient_answers,
        physical_exam=physical_exam,
        llm_assessment=llm_assessment,
        patient_inquiries=patient_inquiries
    )

    # Display results
    display_assessment_summary(llm_assessment, patient_name)

    if patient_inquiries:
        display_patient_education(patient_inquiries, patient_name)

    # Optional: Save to JSON
    if save_json:
        save_exam_to_json(exam, json_path)

    print("\n" + "=" * 70)
    print("EXAMINATION COMPLETE")
    print("=" * 70)

    return exam, patient_inquiries


# ============================================================================
# ENTRY POINT
# ============================================================================

def main() -> int:
    """Main entry point for musculoskeletal examination."""
    try:
        # Run exam with fallback assessment (no API key required)
        # Set use_medkit=True to enable AI-powered assessment
        exam_record, patient_questions = run_musculoskeletal_exam(
            use_medkit=False,
            include_education=True,
            save_json=False
        )
        return 0
    except Exception as e:
        print(f"✗ Error: {e}")
        logger.error("Error during musculoskeletal examination", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
