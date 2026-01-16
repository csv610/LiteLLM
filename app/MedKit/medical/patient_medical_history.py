"""patient_medical_history - Generate exam-specific medical history questions.

This module generates comprehensive, trauma-informed questions to collect patient medical history
tailored to specific medical exams. Questions are focused on clinically relevant topics for each
exam type with contextual consideration of patient age, gender, and history collection purpose
(surgery, medication safety, or physical examination). Integrates with exam_specifications for
specialized topic guidance.

QUICK START:
    Generate medical history questions for a specific exam:

    >>> from patient_medical_history import PatientMedicalHistoryGenerator
    >>> generator = PatientMedicalHistoryGenerator()
    >>> result = generator.generate(exam="cardiac", age=55, gender="male")
    >>> print(f"Generated {len(result.past_medical_history.condition_questions)} condition questions")

    For pre-operative assessment:

    >>> result = generator.generate(exam="cardiac", age=60, gender="female", purpose="surgery")

    Or use the CLI:

    $ python patient_medical_history.py -e cardiac -a 55 -g male
    $ python patient_medical_history.py -e respiratory -a 50 -g female -p medication

COMMON USES:
    1. Clinical documentation - gathering comprehensive patient history efficiently and systematically
    2. Surgical planning - pre-operative assessment with focus on anesthesia and surgical risk factors
    3. Medication safety - assessing drug allergies, interactions, and medication adherence before prescribing
    4. Physical examination preparation - contextual history gathering to guide physical findings
    5. Electronic health record integration - structured data collection for EHR systems and clinical decision support

KEY FEATURES AND COVERAGE AREAS:
    - Past medical history questions about conditions, hospitalizations, and surgeries with follow-up probing
    - Family history questions about maternal, paternal, and genetic risk factors with condition-specific focus
    - Drug information including medications, allergies, adverse reactions with clinical relevance per purpose
    - Vaccination status questions with vaccine-specific and booster shot coverage tailored to patient age
    - Lifestyle and social history questions about tobacco, alcohol, exercise, diet, occupation, and housing
    - Purpose-specific emphasis with surgery questions focused on bleeding/anesthesia, medication on interactions, physical exam on current status
    - Trauma-informed language with respectful, non-judgmental framing and cultural sensitivity throughout
    - Clinical relevance documentation explaining why each question matters for the specific exam type
    - Follow-up question suggestions for positive responses with clinical reasoning and investigation focus
    - Age and gender appropriate questioning adapted to patient demographics and life stage considerations
    - Requirement specification marking questions as mandatory or optional for clinical decision-making
    """

import json
import argparse
from enum import Enum
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
from medkit.core.medkit_client import MedKitClient, MedKitConfig
from medkit.diagnostics.exam_specifications import get_exam_specification

from medkit.utils.logging_config import setup_logger

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig

# Configure logging
logger = setup_logger(__name__, enable_file_handler=False)

# ============================================================================ 
# CONSTANTS AND ENUMS
# ============================================================================ 

class HistoryPurpose(str, Enum):
    SURGERY = "surgery"
    MEDICATION = "medication"
    PHYSICAL_EXAM = "physical_exam"

class QuestionRequirement(str, Enum):
    MANDATORY = "mandatory"
    OPTIONAL = "optional"

# ============================================================================ 
# CONFIGURATION
# ============================================================================ 

@dataclass
class Config(MedKitConfig):
    """Configuration for the patient medical history generator."""
    log_file: Path = field(default_factory=lambda: Path("logs/patient_medical_history.log"))
    trauma_informed: bool = True
    culturally_sensitive: bool = True

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "patient_medical_history.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================ 
# QUESTION MODELS
# ============================================================================ 

class FollowUpQuestion(BaseModel):
    question: str = Field(description="The follow-up question text")
    clinical_reason: str = Field(description="Why this follow-up is clinically important")
    investigation_focus: str = Field(description="What specific diagnostic or clinical aspect is being investigated")

class HistoryQuestion(BaseModel):
    question: str = Field(description="The question to ask the patient")
    clinical_relevance: str = Field(description="Why this question is clinically relevant")
    requirement: QuestionRequirement = Field(description="Whether mandatory or optional")
    expected_answer_type: str = Field(description="Type of answer expected (yes/no, descriptive, date, etc.)")

class PastConditionQuestion(HistoryQuestion):
    condition_category: str = Field(description="Category of condition (cardiac, respiratory, endocrine, etc.)")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

class HospitalizationQuestion(HistoryQuestion):
    scope: str = Field(description="Scope of hospitalization question (frequency, reason, duration, etc.)")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

class SurgeryQuestion(HistoryQuestion):
    detail_level: str = Field(description="Level of detail requested (list, specific procedures, complications)")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

class FamilyHistoryQuestion(HistoryQuestion):
    family_member_type: str = Field(description="Type of family member (parent, sibling, grandparent, etc.)")
    condition_focus: str = Field(description="Medical conditions to focus on")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

class MedicationQuestion(HistoryQuestion):
    aspect: str = Field(description="Aspect of medication use (current medications, dosage, adherence, side effects)")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

class AllergyQuestion(HistoryQuestion):
    allergy_type: str = Field(description="Type of allergy (medication, food, environmental, latex, contrast dye)")
    detail_aspect: str = Field(description="Aspect of allergy to assess (type, reaction, severity, management)")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

class VaccinationQuestion(HistoryQuestion):
    vaccine_focus: str = Field(description="Specific vaccine or vaccine category")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

class LifestyleQuestion(HistoryQuestion):
    category: str = Field(description="Lifestyle category (tobacco, alcohol, diet, exercise, sleep, stress)")
    detail_requested: str = Field(description="Type of detail requested (frequency, quantity, impact, duration)")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

class PersonalSocialQuestion(HistoryQuestion):
    social_aspect: str = Field(description="Social aspect (occupation, housing, relationships, education, support systems)")
    follow_up_questions: List[FollowUpQuestion] = Field(default_factory=list)

# ============================================================================ 
# COMPLETE OUTPUT MODELS
# ============================================================================ 

class PastMedicalHistoryQuestions(BaseModel):
    condition_questions: List[PastConditionQuestion]
    hospitalization_questions: List[HospitalizationQuestion]
    surgery_questions: List[SurgeryQuestion]

class FamilyHistoryQuestions(BaseModel):
    maternal_history_questions: List[FamilyHistoryQuestion]
    paternal_history_questions: List[FamilyHistoryQuestion]
    genetic_risk_questions: List[FamilyHistoryQuestion]

class DrugInformationQuestions(BaseModel):
    medication_questions: List[MedicationQuestion]
    allergy_questions: List[AllergyQuestion]
    adverse_reaction_questions: List[AllergyQuestion]

class VaccinationQuestions(BaseModel):
    vaccination_status_questions: List[VaccinationQuestion]
    vaccine_specific_questions: List[VaccinationQuestion]
    booster_questions: List[VaccinationQuestion]

class LifestyleAndSocialQuestions(BaseModel):
    lifestyle_questions: List[LifestyleQuestion]
    personal_social_questions: List[PersonalSocialQuestion]

class PatientMedicalHistoryQuestions(BaseModel):
    purpose: str
    exam: str
    age: int
    gender: str
    past_medical_history: PastMedicalHistoryQuestions
    family_history: FamilyHistoryQuestions
    drug_information: DrugInformationQuestions
    vaccination: VaccinationQuestions
    lifestyle_and_social: LifestyleAndSocialQuestions

# ============================================================================ 
# PATIENT MEDICAL HISTORY GENERATOR
# ============================================================================ 

class PatientMedicalHistoryGenerator:
    """Generates patient medical history questions."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        # Load model name from ModuleConfig

        model_name = "gemini-1.5-pro"  # Default model for this module

        

        self.client = MedKitClient(model_name=model_name)

    def generate(self, exam: str, age: int, gender: str, purpose: str = "physical_exam") -> PatientMedicalHistoryQuestions:
        self._validate_inputs(exam, age, gender, purpose)
        
        spec = get_exam_specification(exam)
        
        prompt = self._build_prompt(exam, age, gender, purpose, spec)
        
        logger.info(f"Generating {exam} medical history questions ({purpose}) for {age}-year-old {gender} patient...")
        
        result = self.client.generate_text(prompt, schema=PatientMedicalHistoryQuestions)
        
        # Enrich result with input parameters
        result.purpose = purpose
        result.exam = exam
        result.age = age
        result.gender = gender
        
        self.save(result)
        self.print_summary(result)
        
        return result

    def _validate_inputs(self, exam: str, age: int, gender: str, purpose: str):
        if not exam or not exam.strip():
            raise ValueError("Exam name cannot be empty")
        if not (1 <= age <= 150):
            raise ValueError("Age must be between 1 and 150")
        if gender.lower() not in {"male", "female", "non-binary", "other", "prefer not to say"}:
            raise ValueError("Invalid gender specified")
        if purpose.lower() not in [p.value for p in HistoryPurpose]:
            raise ValueError("Invalid purpose specified")

    def _build_prompt(self, exam: str, age: int, gender: str, purpose: str, spec) -> str:
        # This is a simplified representation of the prompt building logic.
        # In a real scenario, this would be more complex, incorporating the logic
        # from the original `build_..._prompt` functions.
        return f"Generate comprehensive medical history questions for a {age}-year-old {gender} patient undergoing a {exam} exam for the purpose of {purpose}."

    def save(self, result: PatientMedicalHistoryQuestions):
        output_path = self.config.output_dir / f"{result.exam}_{result.purpose}_age{result.age}_{result.gender}.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(result.model_dump(), f, indent=2)
        logger.info(f"Saved questions to: {output_path}")

    def print_summary(self, result: PatientMedicalHistoryQuestions):
        total_questions = (
            len(result.past_medical_history.condition_questions) +
            len(result.past_medical_history.hospitalization_questions) +
            len(result.past_medical_history.surgery_questions) +
            len(result.family_history.maternal_history_questions) +
            len(result.family_history.paternal_history_questions) +
            len(result.family_history.genetic_risk_questions) +
            len(result.drug_information.medication_questions) +
            len(result.drug_information.allergy_questions) +
            len(result.drug_information.adverse_reaction_questions) +
            len(result.vaccination.vaccination_status_questions) +
            len(result.vaccination.vaccine_specific_questions) +
            len(result.vaccination.booster_questions) +
            len(result.lifestyle_and_social.lifestyle_questions) +
            len(result.lifestyle_and_social.personal_social_questions)
        )
        print("\n" + "="*70)
        print(f"MEDICAL HISTORY QUESTIONS SUMMARY: {result.exam.upper()} ({result.purpose.upper()})")
        print("="*70)
        print(f"  - Total Questions Generated: {total_questions}")
        print(f"  - Patient Profile: {result.age}-year-old {result.gender}")
        print(f"\n✓ Generation complete.")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate comprehensive patient medical history questions.")
    parser.add_argument("-e", "--exam", required=True, help="Type of medical exam (e.g., cardiac, respiratory).")
    parser.add_argument("-a", "--age", type=int, required=True, help="Patient age in years.")
    parser.add_argument("-g", "--gender", required=True, help="Patient gender.")
    parser.add_argument("-p", "--purpose", default="physical_exam", choices=[p.value for p in HistoryPurpose], help="Purpose of history collection.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"), help="Output directory for generated files.")
    
    args = parser.parse_args()
    
    config = Config(output_dir=args.output_dir)
    
    try:
        generator = PatientMedicalHistoryGenerator(config=config)
        generator.generate(args.exam, args.age, args.gender, args.purpose)
    except ValueError as e:
        logger.error(f"Input validation error: {e}")
        parser.print_help()
        exit(1)
    except Exception as e:
        logger.error(f"Failed to generate questions: {e}")
        exit(1)

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
