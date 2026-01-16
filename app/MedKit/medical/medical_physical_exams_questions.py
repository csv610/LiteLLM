"""medical_physical_exams_questions - Generate structured physical examination questions.

This module generates comprehensive, clinically-relevant questions for different types of
physical examinations. It creates questions across multiple examination techniques
(inspection, palpation, percussion, auscultation) and includes assessment questions for
medical history, lifestyle, and family history.

Age and gender are now essential parameters to ensure questions are appropriate and
relevant to the specific patient profile.

QUICK START:
    Generate physical exam questions with patient demographics:

    >>> from medical_physical_exams_questions import ExamQuestionGenerator
    >>> generator = ExamQuestionGenerator()
    >>> result = generator.generate("Cardiovascular Exam", age=55, gender="Female")
    >>> print(result.exam_type)
    Cardiovascular Exam
    >>> print(result.age)
    55
    >>> print(result.gender)
    Female

    Or use the CLI:

    $ python medical_physical_exams_questions.py -e "Respiratory Exam" -a 45 -g "Male"
    $ python medical_physical_exams_questions.py -e "Abdominal Exam" -a 8 -g "Female" -o custom_output.json -v

COMMON USES:
    1. Medical education - teaching proper physical exam techniques tailored to patient age/gender
    2. Clinical training - standardizing exam question protocols for diverse patient populations
    3. Patient interviews - structured history and assessment questions appropriate for age/gender
    4. Quality assurance - ensuring comprehensive exam coverage with age/gender considerations
"""

import json
import sys
import logging
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional
from pydantic import BaseModel, Field

from medkit.core.medkit_client import MedKitClient, MedKitConfig
from medkit.utils.logging_config import setup_logger

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig

logger = setup_logger(__name__, enable_file_handler=True)

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class Config(MedKitConfig):
    """Configuration for the physical exam question generator."""
    output_dir: Path = field(default_factory=lambda: Path(__file__).parent / "outputs")


    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "medical_physical_exams_questions.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================
# EXAM-SPECIFIC CLINICAL GUIDANCE
# ============================================================================

EXAMS_WITH_REPRODUCTIVE_RELEVANCE = {
    "Skin Exam",
    "Eye Exam",
    "Gynecological Exam",
    "Obstetric Exam",
    "Genitourinary Exam",
    "Infectious Disease Assessment",
    "Endocrine Exam"
}

EXAMS_WITH_STRESS_RELEVANCE = {
    "Skin Exam",
    "Eye Exam",
    "Abdominal Exam",
    "Respiratory Exam",
    "Cardiovascular Exam",
    "Neurological Exam",
    "Musculoskeletal Exam",
    "Mental Health Assessment"
}

EXAM_SPECIFIC_FOCUS = {
    "Skin Exam": [
        "face and acne distribution patterns",
        "intertriginous areas (folds)",
        "extremities and nails",
        "scalp and hairline"
    ],
    "Respiratory Exam": [
        "upper lobes bilaterally",
        "lower lobes bilaterally",
        "breath sound distribution and character",
        "accessory muscle use"
    ],
    "Cardiovascular Exam": [
        "precordium and point of maximal impulse",
        "murmur location and radiation",
        "peripheral pulses bilaterally",
        "jugular venous pressure"
    ],
    "Abdominal Exam": [
        "right upper quadrant",
        "left upper quadrant",
        "right lower quadrant",
        "left lower quadrant",
        "periumbilical region"
    ],
    "Neurological Exam": [
        "cranial nerve distributions",
        "motor strength by extremity",
        "sensory levels and dermatomes",
        "reflex asymmetries"
    ],
    "Musculoskeletal Exam": [
        "bilateral joint comparison",
        "range of motion limitations",
        "muscle atrophy or hypertrophy",
        "joint swelling and warmth"
    ]
}


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


class ExamQuestionGenerator:
    """Generates comprehensive physical examination questions using LLM.

    This class uses the MedKitClient to generate clinically-relevant questions for
    various types of physical examinations, organized by examination technique.
    """

    def __init__(self, client: Optional[MedKitClient] = None, config: Optional[Config] = None):
        """Initialize the exam question generator.

        Args:
            client: Optional MedKitClient instance. If None, creates a new one.
            config: Optional Config instance. If None, creates a new one with defaults.
        """
        # Load model name from ModuleConfig if client not provided

        if client is None:

            model_name = "gemini-1.5-flash"  # Default model for this module

            client = MedKitClient(model_name=model_name)

        

        self.client = client
        self.config = config or Config()
        self.exam_type: Optional[str] = None
        self.age: Optional[int] = None
        self.gender: Optional[str] = None
        self.output_path: Optional[Path] = None

        # Apply verbosity level to logger
        verbosity_levels = {0: "CRITICAL", 1: "ERROR", 2: "WARNING", 3: "INFO", 4: "DEBUG"}
        logger.setLevel(verbosity_levels.get(self.config.verbosity, "WARNING"))
        logging.getLogger("medkit").setLevel(verbosity_levels.get(self.config.verbosity, "WARNING"))

    def generate(self, exam_type: str, age: Optional[int] = None, gender: Optional[str] = None, output_path: Optional[Path] = None) -> ExamQuestions:
        """Generate physical examination questions for a specific exam type.

        Args:
            exam_type: The type of physical exam (e.g., "Cardiovascular Exam", "Respiratory Exam")
            age: Optional age of the patient in years.
            gender: Optional gender of the patient (e.g., "Male", "Female", "Other").
            output_path: Optional path to save the JSON output.

        Returns:
            ExamQuestions object containing organized questions.

        Raises:
            ValueError: If exam_type is empty.
        """
        if not exam_type or not exam_type.strip():
            raise ValueError("Exam type cannot be empty")

        self.exam_type = exam_type
        self.age = age
        self.gender = gender

        if output_path is None:
            output_path = self.config.output_dir / f"{exam_type.lower().replace(' ', '_')}_phyexam_qa.json"

        self.output_path = output_path

        patient_info = f"{exam_type}"
        if age is not None and gender is not None:
            patient_info += f" (Age: {age}, Gender: {gender})"
        elif age is not None:
            patient_info += f" (Age: {age})"
        elif gender is not None:
            patient_info += f" (Gender: {gender})"

        logger.info(f"Generating physical exam questions for: {patient_info}")

        exam_questions = self._generate_questions()
        self.save(exam_questions, self.output_path)
        self.print_summary(exam_questions)

        return exam_questions

    def _should_include_reproductive_health(self) -> bool:
        """Determine if reproductive/hormonal health questions should be included."""
        if self.exam_type not in EXAMS_WITH_REPRODUCTIVE_RELEVANCE:
            return False

        # Include for females of reproductive age (13-50)
        if self.gender and self.gender.lower() in ["female", "woman"]:
            if self.age is None or (13 <= self.age <= 50):
                return True

        # Include for males in applicable exams
        if self.gender and self.gender.lower() in ["male", "man"]:
            if self.exam_type in ["Genitourinary Exam", "Endocrine Exam", "Infectious Disease Assessment"]:
                return True

        return False

    def _get_reproductive_health_guidance(self) -> str:
        """Get reproductive/hormonal health guidance based on gender and age."""
        guidance = ""

        if self.gender and self.gender.lower() in ["female", "woman"]:
            guidance += "FEMALE REPRODUCTIVE/HORMONAL HEALTH CONSIDERATIONS:\n"
            guidance += "- Ask about menstrual cycle regularity, duration, and any abnormalities\n"
            guidance += "- Explore temporal relationships between menstrual cycle and presenting symptoms (common for skin, mood, pain conditions)\n"
            guidance += "- Ask about pregnancy status, pregnancy plans, and breastfeeding\n"
            guidance += "- Consider effects of hormonal contraceptives or hormone replacement therapy on findings\n"
            if self.age and self.age < 40:
                guidance += "- Young women may present with acne, eczema flares, or other conditions exacerbated by hormonal cycles\n"
            if self.age and self.age >= 40:
                guidance += "- Consider perimenopausal or menopausal symptoms that may affect exam findings\n"

        elif self.gender and self.gender.lower() in ["male", "man"]:
            guidance += "MALE REPRODUCTIVE/HORMONAL HEALTH CONSIDERATIONS:\n"
            guidance += "- Ask about erectile function, libido, and any changes in sexual health\n"
            guidance += "- Explore any changes in body or facial hair distribution\n"
            guidance += "- Consider testosterone levels and hormone-related conditions\n"

        return guidance

    def _should_include_stress_assessment(self) -> bool:
        """Determine if stress/psychological assessment should be included."""
        return self.exam_type in EXAMS_WITH_STRESS_RELEVANCE

    def _get_stress_assessment_guidance(self) -> str:
        """Get stress/psychological assessment guidance."""
        return """STRESS AND PSYCHOLOGICAL FACTORS:
- Ask about current stress levels and major life stressors
- Explore the temporal relationship between stress and symptom onset/exacerbation
- Ask about sleep quality, mood, anxiety, and emotional state
- Inquire about the psychological impact of symptoms on quality of life, social functioning, and work
- Consider whether symptoms improve or worsen with stress management or relaxation
- For psychosomatic presentations, explore both physical and emotional factors
"""

    def _get_exam_specific_focus_guidance(self) -> str:
        """Get exam-specific anatomical focus guidance."""
        if self.exam_type not in EXAM_SPECIFIC_FOCUS:
            return ""

        guidance = f"\nEXAM-SPECIFIC FOCUS AREAS FOR {self.exam_type.upper()}:\n"
        guidance += "Ensure detailed assessment of the following areas:\n"
        for area in EXAM_SPECIFIC_FOCUS[self.exam_type]:
            guidance += f"- {area}\n"
        guidance += "Include both general and site-specific questions to ensure comprehensive coverage.\n"

        return guidance

    def _generate_questions(self) -> ExamQuestions:
        """Generate exam questions using the LLM with structured schema.

        Returns:
            ExamQuestions object with generated questions organized by technique.
        """
        # Build patient context string
        patient_context = ""
        if self.age is not None or self.gender is not None:
            patient_context = "\n\nPATIENT CONTEXT:\n"
            if self.age is not None:
                patient_context += f"- Age: {self.age} years old\n"
                # Add age-specific guidance
                if self.age < 18:
                    patient_context += "- Patient is a pediatric patient - consider developmental stage and special considerations for children\n"
                elif self.age >= 65:
                    patient_context += "- Patient is an elderly patient - consider age-related changes and geriatric-specific conditions\n"
            if self.gender is not None:
                patient_context += f"- Gender: {self.gender}\n"
                # Add gender-specific guidance
                if self.gender.lower() in ["female", "woman"]:
                    patient_context += "- For applicable exams, consider gender-specific health conditions and reproductive health factors\n"
                elif self.gender.lower() in ["male", "man"]:
                    patient_context += "- For applicable exams, consider gender-specific health conditions and reproductive health factors\n"
            patient_context += "- Ensure questions are appropriate and sensitive to the patient's age and gender\n"

        # Build exam-specific considerations
        exam_considerations = ""

        if self._should_include_reproductive_health():
            exam_considerations += "\n" + self._get_reproductive_health_guidance()

        if self._should_include_stress_assessment():
            exam_considerations += "\n" + self._get_stress_assessment_guidance()

        exam_considerations += self._get_exam_specific_focus_guidance()

        prompt = f"""Generate comprehensive physical examination questions for: {self.exam_type}{patient_context}{exam_considerations}

Create detailed, clinically-relevant questions organized by examination technique:

1. INSPECTION QUESTIONS: Questions about visual findings, appearance, symmetry, color, texture, etc.
   - Include 4-6 specific questions about what to observe
   - Format each question as: "Q1: [question]", "Q2: [question]", etc.

2. PALPATION QUESTIONS: Questions about findings when palpating/touching the examined area
   - Include 4-6 specific questions about texture, temperature, masses, tenderness, etc.
   - Format each question as: "Q1: [question]", "Q2: [question]", etc.

3. PERCUSSION QUESTIONS: Questions related to percussion technique if applicable
   - Include 3-4 questions (if not applicable, provide empty list)
   - Format each question as: "Q1: [question]", "Q2: [question]", etc.

4. AUSCULTATION QUESTIONS: Questions about sounds heard with stethoscope if applicable
   - Include 4-6 questions (if not applicable, provide empty list)
   - Format each question as: "Q1: [question]", "Q2: [question]", etc.

5. VERBAL ASSESSMENT QUESTIONS: Open-ended questions for patient communication and symptoms
   - Include 5-6 questions about pain, symptoms, duration, triggers, etc.
   - Format each question as: "Q1: [question]", "Q2: [question]", etc.

6. MEDICAL HISTORY QUESTIONS: Questions about past medical conditions relevant to this exam
   - Include 4-5 questions about relevant medical conditions and treatments
   - Format each question as: "Q1: [question]", "Q2: [question]", etc.

7. LIFESTYLE QUESTIONS: Questions about lifestyle factors that may affect findings
   - Include 4-5 questions about habits, activities, exposure, etc.
   - Format each question as: "Q1: [question]", "Q2: [question]", etc.

8. FAMILY HISTORY QUESTIONS: Questions about family history relevant to this exam
   - Include 3-4 questions about family conditions and genetic factors
   - Format each question as: "Q1: [question]", "Q2: [question]", etc.

Ensure all questions are:
- Clinically appropriate and evidence-based
- Clear and easy to understand by medical students and clinicians
- Specific to the {self.exam_type}
- Practical for use in clinical settings"""

        result = self.client.generate_text(
            prompt,
            schema=ExamQuestions
        )
        return result

    def save(self, exam_questions: ExamQuestions, output_path: Path) -> Path:
        """Save the generated exam questions to a JSON file.

        Args:
            exam_questions: The ExamQuestions object to save.
            output_path: Path where the JSON file should be saved.

        Returns:
            Path to the saved file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(exam_questions.model_dump(), f, indent=2)

        logger.info(f"✓ Exam questions saved to {output_path}")
        return output_path

    def print_summary(self, exam_questions: ExamQuestions) -> None:
        """Log a summary of the generated exam questions.

        Args:
            exam_questions: The ExamQuestions object to summarize.
        """
        if not self.config.verbose:
            return

        summary = f"PHYSICAL EXAM QUESTIONS: {exam_questions.exam_type}\n"
        summary += f"  Inspection questions:        {len(exam_questions.inspection_questions)}\n"
        summary += f"  Palpation questions:         {len(exam_questions.palpation_questions)}\n"
        summary += f"  Percussion questions:        {len(exam_questions.percussion_questions)}\n"
        summary += f"  Auscultation questions:      {len(exam_questions.auscultation_questions)}\n"
        summary += f"  Verbal assessment questions: {len(exam_questions.verbal_assessment_questions)}\n"
        summary += f"  Medical history questions:   {len(exam_questions.medical_history_questions)}\n"
        summary += f"  Lifestyle questions:         {len(exam_questions.lifestyle_questions)}\n"
        summary += f"  Family history questions:    {len(exam_questions.family_history_questions)}\n"
        total = sum([
            len(exam_questions.inspection_questions),
            len(exam_questions.palpation_questions),
            len(exam_questions.percussion_questions),
            len(exam_questions.auscultation_questions),
            len(exam_questions.verbal_assessment_questions),
            len(exam_questions.medical_history_questions),
            len(exam_questions.lifestyle_questions),
            len(exam_questions.family_history_questions)
        ])
        summary += f"\n  Total questions: {total}\n"
        summary += f"  Questions saved to {self.output_path}"
        logger.info(summary)


def generate_exam_questions(exam_type: str, age: Optional[int] = None, gender: Optional[str] = None, output_path: Optional[Path] = None, verbose: bool = False) -> ExamQuestions:
    """High-level function to generate and save exam questions.

    Args:
        exam_type: The type of physical exam.
        age: Optional age of the patient in years.
        gender: Optional gender of the patient.
        output_path: Optional path to save the output JSON file.
        verbose: Whether to show verbose console output.

    Returns:
        The generated ExamQuestions object.
    """
    config = Config(verbose=verbose)
    generator = ExamQuestionGenerator(config=config)
    return generator.generate(exam_type, age, gender, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate comprehensive physical examination questions."
    )
    parser.add_argument(
        "-i", "--exam",
        type=str,
        required=True,
        help="The type of physical exam (e.g., 'Cardiovascular Exam', 'Respiratory Exam')"
    )
    parser.add_argument(
        "-a", "--age",
        type=int,
        required=True,
        help="Age of the patient in years"
    )
    parser.add_argument(
        "-g", "--gender",
        type=str,
        required=True,
        help="Gender of the patient (e.g., 'Male', 'Female', 'Other')"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Optional: The path to save the output JSON file."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show verbose console output."
    )

    args = parser.parse_args()

    output_path = Path(args.output) if args.output else None
    result = generate_exam_questions(args.exam, args.age, args.gender, output_path, args.verbose)
    logger.info(f"Success: Questions generated and saved.")


    def close(self):
        """Close LMDB storage and release resources."""
        if self.storage:
            try:
                self.storage.close()
                logger.info("LMDB storage closed successfully.")
            except Exception as e:
                logger.error(f"Error closing LMDB storage: {e}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
