"""
Musculoskeletal Telemedicine Exam - MVP
Simplified version for rapid testing and iteration.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# ============================================================================
# DATA MODELS (Simplified)
# ============================================================================

class Exam(BaseModel):
    patient_name: str = "Unknown"
    patient_id: str
    encounter_id: str
    timestamp: datetime
    answers: dict
    physical_exam: dict
    assessment: dict


# ============================================================================
# QUESTIONS (Combined into logical groups)
# ============================================================================

QUESTIONS = {
    "patient_info": [
        ("name", "Patient Name (press Enter for 'Unknown'): "),
    ],
    "red_flags": [
        ("fever", "Fever, chills, or night sweats in past month? "),
        ("weight_loss", "Unexplained weight loss (>10 lbs) in past 3 months? "),
        ("neurologic", "Progressive numbness/weakness spreading down legs? "),
        ("bowel_bladder", "Changes in bowel/bladder control or saddle numbness? "),
        ("swelling_unilateral", "Severe one-sided leg swelling with calf pain? "),
        ("pain_rest", "Severe pain at rest that doesn't improve? "),
        ("trauma_high", "High-energy trauma, major fall, or MVA? "),
        ("systemic", "Rash, sore throat, recent infection, or constitutional symptoms? "),
    ],
    "medications": [
        ("allergies", "Drug allergies or intolerances? "),
        ("medications", "Current medications (name, dose, frequency)? "),
        ("supplements", "Vitamins, supplements, or herbals? "),
    ],
    "history": [
        ("previous_surgery", "Previous surgery on this joint? "),
        ("previous_problems", "Previous injuries or chronic pain in this area? "),
        ("autoimmune", "Autoimmune conditions (RA, lupus, etc.)? "),
    ],
    "pain_assessment": [
        ("pain_location", "Where is your pain? "),
        ("pain_onset", "When did it start? "),
        ("pain_severity", "Pain severity (0-10 scale)? "),
        ("pain_quality", "Describe pain (sharp, dull, aching, throbbing)? "),
        ("pain_worse", "What makes it worse? "),
        ("pain_better", "What makes it better? "),
    ],
    "functional": [
        ("swelling", "Swelling, redness, warmth, or stiffness? "),
        ("movement", "Limitation in joint movements or daily activities? "),
        ("weakness", "Weakness in muscles or difficulty lifting? "),
    ],
}

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
# QUESTION COLLECTION
# ============================================================================

def collect_responses(question_dict: dict) -> dict:
    """Collect patient responses to a dictionary of questions."""
    responses = {}
    for q_id, question in question_dict:
        answer = input(question).strip()
        responses[q_id] = answer or "(no response)"
    return responses


def collect_exam() -> dict:
    """Collect complete musculoskeletal exam."""
    print("\n" + "=" * 60)
    print("MUSCULOSKELETAL EXAMINATION")
    print("=" * 60)

    exam = {}

    # Inspection
    exam["inspection"] = input("\nInspection findings (swelling, redness, deformity): ").strip()

    # Palpation
    exam["palpation"] = input("Palpation findings (tenderness, warmth, crepitus): ").strip()

    # Range of motion
    exam["range_of_motion"] = input("Range of motion (active/passive, joints tested): ").strip()

    # Strength
    exam["strength"] = input("Strength testing (0-5 grading, muscle groups): ").strip()

    # Gait
    exam["gait"] = input("Gait observation (walking pattern, posture): ").strip()

    # Special tests
    exam["special_tests"] = input("Special tests performed (Lachman, McMurray, etc.): ").strip()

    return exam


def generate_assessment(answers: dict, exam: dict) -> dict:
    """Generate simple clinical assessment."""
    # Check for red flags
    red_flags = []
    if answers.get("fever", "").lower().startswith("y"):
        red_flags.append("Fever/night sweats reported")
    if answers.get("weight_loss", "").lower().startswith("y"):
        red_flags.append("Unexplained weight loss reported")
    if answers.get("bowel_bladder", "").lower().startswith("y"):
        red_flags.append("⚠️  BOWEL/BLADDER CHANGES - Needs urgent evaluation")

    # Basic assessment
    assessment = {
        "red_flags": red_flags,
        "primary_impression": "Musculoskeletal examination findings documented. Further evaluation recommended.",
        "urgency": "urgent" if red_flags else "monitor",
        "recommendations": [
            "Physical therapy evaluation",
            "Activity modification as tolerated",
            "Follow-up in 2 weeks",
        ]
    }

    return assessment


def generate_patient_education(assessment: dict) -> dict:
    """Generate simple patient education responses."""
    urgency = assessment.get("urgency", "monitor")

    education = {}
    education["diagnosis"] = f"Based on exam: {assessment.get('primary_impression')}. Your physician will provide specific diagnosis."
    education["timeline"] = "Recovery varies (typically 2-6 weeks). Your physician will give specific timeline."
    education["permanent"] = "Most musculoskeletal conditions are manageable. Permanent disability is rare with proper treatment."
    education["treatment"] = f"Recommendations: {', '.join(assessment.get('recommendations', []))}"
    education["alternatives"] = "Physical therapy is excellent. Discuss supplements with your physician."
    education["activity"] = "Avoid activities that significantly increase pain. Gradually return as tolerated."
    education["prevention"] = "Regular exercise, good posture, proper ergonomics, weight management."
    education["lifestyle"] = "Exercise regularly, sleep 7-9 hours, manage stress, eat anti-inflammatory foods."
    education["complications"] = "Rare with proper treatment. Your physician will monitor you."
    education["specialist"] = "Appropriate if symptoms don't improve in 4 weeks. Ask your physician for referral."

    return education


def run_exam() -> Exam:
    """Main exam workflow."""
    print("\n" + "=" * 60)
    print("MUSCULOSKELETAL TELEMEDICINE EXAM")
    print("=" * 60)

    # Patient info
    print("\n--- PATIENT INFORMATION ---")
    patient_name = input("Patient Name (default: Unknown): ").strip() or "Unknown"

    # Red flags
    print("\n--- RED FLAG SCREENING (Answer Y/N) ---")
    red_flag_answers = collect_responses(QUESTIONS["red_flags"])

    # Medications
    print("\n--- MEDICATIONS & ALLERGIES ---")
    med_answers = collect_responses(QUESTIONS["medications"])

    # History
    print("\n--- MEDICAL HISTORY ---")
    history_answers = collect_responses(QUESTIONS["history"])

    # Pain assessment
    print("\n--- PAIN ASSESSMENT ---")
    pain_answers = collect_responses(QUESTIONS["pain_assessment"])

    # Functional
    print("\n--- FUNCTIONAL STATUS ---")
    func_answers = collect_responses(QUESTIONS["functional"])

    # Combine all answers
    all_answers = {
        **red_flag_answers,
        **med_answers,
        **history_answers,
        **pain_answers,
        **func_answers,
    }

    # Physical exam
    physical_exam = collect_exam()

    # Assessment
    assessment = generate_assessment(all_answers, physical_exam)

    # Patient education
    education = generate_patient_education(assessment)

    # Create exam record
    exam = Exam(
        patient_name=patient_name,
        patient_id=f"MSK{datetime.now().strftime('%Y%m%d%H%M')}",
        encounter_id=f"ENC{datetime.now().strftime('%Y%m%d%H%M%S')}",
        timestamp=datetime.now(),
        answers=all_answers,
        physical_exam=physical_exam,
        assessment=assessment,
    )

    # Display results
    print("\n" + "=" * 60)
    print(f"ASSESSMENT SUMMARY - {patient_name}")
    print("=" * 60)

    if assessment["red_flags"]:
        print("\n⚠️  RED FLAGS DETECTED:")
        for flag in assessment["red_flags"]:
            print(f"   • {flag}")

    print(f"\n📋 Primary Impression: {assessment['primary_impression']}")
    print(f"⚠️  Urgency: {assessment['urgency'].upper()}")
    print("\n💊 Recommendations:")
    for rec in assessment["recommendations"]:
        print(f"   • {rec}")

    # Patient education
    print("\n" + "=" * 60)
    print("ANSWERS TO PATIENT QUESTIONS")
    print("=" * 60)
    for q_id, question in PATIENT_QUESTIONS:
        print(f"\nQ: {question}")
        print(f"A: {education.get(q_id, 'Consult with your physician.')}\n")

    # Save option
    if input("\nSave exam to JSON? (y/n): ").lower() == "y":
        import json
        filename = f"exam_{exam.encounter_id}.json"
        with open(filename, "w") as f:
            json.dump(exam.model_dump(mode="json"), f, indent=2, default=str)
        print(f"✓ Saved to {filename}")

    return exam


if __name__ == "__main__":
    run_exam()
