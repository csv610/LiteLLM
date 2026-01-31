"""medical_physical_exams_questions - Generate structured physical examination questions."""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Optional

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response
from utils.output_formatter import print_result

from medical_physical_exams_questions_models import ExamQuestions

EXAMS_WITH_REPRODUCTIVE_RELEVANCE = {
    "Skin Exam", "Eye Exam", "Gynecological Exam", "Obstetric Exam",
    "Genitourinary Exam", "Infectious Disease Assessment", "Endocrine Exam"
}

EXAMS_WITH_STRESS_RELEVANCE = {
    "Skin Exam", "Eye Exam", "Abdominal Exam", "Respiratory Exam",
    "Cardiovascular Exam", "Neurological Exam", "Musculoskeletal Exam",
    "Mental Health Assessment"
}

EXAM_SPECIFIC_FOCUS = {
    "Skin Exam": ["face and acne distribution patterns", "intertriginous areas (folds)", "extremities and nails", "scalp and hairline"],
    "Respiratory Exam": ["upper lobes bilaterally", "lower lobes bilaterally", "breath sound distribution and character", "accessory muscle use"],
    "Cardiovascular Exam": ["precordium and point of maximal impulse", "murmur location and radiation", "peripheral pulses bilaterally", "jugular venous pressure"],
    "Abdominal Exam": ["right upper quadrant", "left upper quadrant", "right lower quadrant", "left lower quadrant", "periumbilical region"],
    "Neurological Exam": ["cranial nerve distributions", "motor strength by extremity", "sensory levels and dermatomes", "reflex asymmetries"],
    "Musculoskeletal Exam": ["bilateral joint comparison", "range of motion limitations", "muscle atrophy or hypertrophy", "joint swelling and warmth"]
}

class ExamQuestionGenerator:
    """Generates comprehensive physical examination questions using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the exam question generator."""
        self.client = LiteClient(model_config=model_config)
        self.exam_type: Optional[str] = None
        self.age: Optional[int] = None
        self.gender: Optional[str] = None

    def generate_text(self, exam_type: str, age: int, gender: str) -> ExamQuestions:
        """Generate physical examination questions for a specific exam type."""
        if not exam_type or not exam_type.strip():
            raise ValueError("Exam type cannot be empty")

        self.exam_type = exam_type
        self.age = age
        self.gender = gender

        prompt = self._create_prompt()
        model_input = ModelInput(user_prompt=prompt, response_format=ExamQuestions)
        result = self._ask_llm(model_input)
        return result

    def _ask_llm(self, model_input: ModelInput) -> ExamQuestions:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)

    def _create_prompt(self) -> str:
        """Generate the prompt for question generation."""
        patient_context = f"\n\nPATIENT CONTEXT:\n- Age: {self.age} years old\n- Gender: {self.gender}\n"
        if self.age < 18:
            patient_context += "- Patient is a pediatric patient - consider developmental stage.\n"
        elif self.age >= 65:
            patient_context += "- Patient is an elderly patient - consider geriatric-specific conditions.\n"

        exam_considerations = ""
        if self.exam_type in EXAMS_WITH_REPRODUCTIVE_RELEVANCE:
            exam_considerations += "\nREPRODUCTIVE/HORMONAL HEALTH CONSIDERATIONS: Ask about cycles, pregnancy, or changes in sexual health as applicable.\n"
        if self.exam_type in EXAMS_WITH_STRESS_RELEVANCE:
            exam_considerations += "\nSTRESS AND PSYCHOLOGICAL FACTORS: Inquire about current stress levels and impact on health.\n"

        if self.exam_type in EXAM_SPECIFIC_FOCUS:
            exam_considerations += f"\nEXAM-SPECIFIC FOCUS AREAS FOR {self.exam_type.upper()}:\n"
            for area in EXAM_SPECIFIC_FOCUS[self.exam_type]:
                exam_considerations += f"- {area}\n"

        return f"""Generate comprehensive physical examination questions for: {self.exam_type}{patient_context}{exam_considerations}

Create detailed, clinically-relevant questions organized by technique:
1. INSPECTION: Visual findings, appearance, symmetry.
2. PALPATION: Texture, temperature, masses, tenderness.
3. PERCUSSION: Technique and findings.
4. AUSCULTATION: Listening with stethoscope.
5. VERBAL ASSESSMENT: Symptoms, pain, triggers.
6. MEDICAL HISTORY: Relevant past conditions.
7. LIFESTYLE: Habits, activities, exposure.
8. FAMILY HISTORY: Genetic factors.

Ensure all questions are clinically appropriate, clear, and age/gender sensitive."""



def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive physical examination questions.")
    parser.add_argument("-i", "--exam", required=True, help="Type of physical exam (e.g., 'Cardiovascular Exam')")
    parser.add_argument("-a", "--age", type=int, required=True, help="Age of the patient in years")
    parser.add_argument("-g", "--gender", required=True, help="Gender of the patient")
    parser.add_argument("-o", "--output", type=Path, help="Path to save JSON output.")
    parser.add_argument("-m", "--model", default="gemini-1.5-pro", help="Model to use (default: gemini-1.5-pro)")

    args = parser.parse_args()

    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        generator = ExamQuestionGenerator(model_config=model_config)
        print(f"Generating physical exam questions...")
        result = generator.generate_text(exam_type=args.exam, age=args.age, gender=args.gender)
        
        print_result(result, title="Medical Physical Exam Questions")
        
        if args.output:
            save_model_response(result, args.output)
            print(f"✓ Questions saved to {args.output}")

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
