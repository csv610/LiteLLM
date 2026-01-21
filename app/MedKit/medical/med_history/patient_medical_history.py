"""patient_medical_history.py - Generate exam-specific medical history questions."""

import json
import sys
import argparse
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

from patient_medical_history_models import PatientMedicalHistoryQuestions, HistoryPurpose

class PatientMedicalHistoryGenerator:
    """Generates patient medical history questions using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.client = LiteClient(model_config=model_config)

    def generate_text(self, exam: str, age: int, gender: str, purpose: str = "physical_exam") -> PatientMedicalHistoryQuestions:
        """Generate patient medical history questions."""
        self._validate_inputs(exam, age, gender, purpose)

        model_input = ModelInput(
            user_prompt=self._create_prompt(exam, age, gender, purpose),
            response_format=PatientMedicalHistoryQuestions,
            system_prompt="You are an expert medical documentation specialist. Generate trauma-informed, clinically relevant medical history questions."
        )

        result = self._ask_llm(model_input)
        
        # Ensure input params are mirrored in result
        result.purpose = purpose
        result.exam = exam
        result.age = age
        result.gender = gender
        
        return result

    def _ask_llm(self, model_input: ModelInput) -> PatientMedicalHistoryQuestions:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)

    def _create_prompt(self, exam: str, age: int, gender: str, purpose: str) -> str:
        """Generate the prompt for history questions."""
        return f"""Generate comprehensive medical history questions for a {age}-year-old {gender} patient undergoing a {exam} exam for the purpose of {purpose}.

The questions should be:
1. Trauma-informed: Respectful, non-judgmental, and culturally sensitive.
2. Purpose-specific: 
   - 'surgery': Focus on anesthesia risk, bleeding, and recovery.
   - 'medication': Focus on allergies, interactions, and adherence.
   - 'physical_exam': Focus on current status and systematic review.
3. Clinically relevant: Explain why each question matters for the {exam} exam.
4. Comprehensive: Include past history, family history, drug info, vaccinations, and lifestyle/social factors.

Provide follow-up questions for positive responses to key clinical indicators."""

    def _validate_inputs(self, exam: str, age: int, gender: str, purpose: str):
        if not exam or not exam.strip():
            raise ValueError("Exam name cannot be empty")
        if not (1 <= age <= 150):
            raise ValueError("Age must be between 1 and 150")
        if purpose not in [p.value for p in HistoryPurpose]:
            raise ValueError(f"Invalid purpose specify one of: {[p.value for p in HistoryPurpose]}")

    def print_result(self, result: PatientMedicalHistoryQuestions) -> None:
        """Print a summary of the generated questions using rich."""
        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table
        
        console = Console()
        console.print(Panel(
            f"[bold]Exam:[/bold] {result.exam.upper()}\n"
            f"[bold]Purpose:[/bold] {result.purpose.upper()}\n"
            f"[bold]Patient:[/bold] {result.age}y {result.gender}",
            title="Patient Medical History Question Set",
            border_style="magenta"
        ))

        table = Table(title="Question Categories")
        table.add_column("Category", style="cyan")
        table.add_column("Count", justify="right", style="green")

        counts = {
            "Past Conditions": len(result.past_medical_history.condition_questions),
            "Hospitalizations": len(result.past_medical_history.hospitalization_questions),
            "Surgeries": len(result.past_medical_history.surgery_questions),
            "Family History": len(result.family_history.maternal_history_questions) + len(result.family_history.paternal_history_questions) + len(result.family_history.genetic_risk_questions),
            "Medications/Allergies": len(result.drug_information.medication_questions) + len(result.drug_information.allergy_questions),
            "Vaccinations": len(result.vaccination.vaccination_status_questions) + len(result.vaccination.vaccine_specific_questions),
            "Lifestyle/Social": len(result.lifestyle_and_social.lifestyle_questions) + len(result.lifestyle_and_social.personal_social_questions)
        }

        for cat, count in counts.items():
            table.add_row(cat, str(count))

        console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive patient medical history questions.")
    parser.add_argument("-e", "--exam", required=True, help="Type of medical exam (e.g., cardiac, respiratory)")
    parser.add_argument("-a", "--age", type=int, required=True, help="Patient age in years")
    parser.add_argument("-g", "--gender", required=True, help="Patient gender")
    parser.add_argument("-p", "--purpose", default="physical_exam", choices=[p.value for p in HistoryPurpose], help="Purpose of history collection")
    parser.add_argument("-o", "--output", type=Path, help="Path to save JSON output.")
    parser.add_argument("-m", "--model", default="gemini-1.5-pro", help="Model to use (default: gemini-1.5-pro)")

    args = parser.parse_args()

    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        generator = PatientMedicalHistoryGenerator(model_config=model_config)
        print(f"Generating medical history questions for {args.exam} ({args.purpose})...")
        result = generator.generate_text(exam=args.exam, age=args.age, gender=args.gender, purpose=args.purpose)
        
        generator.print_result(result)
        
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, 'w') as f:
                json.dump(result.model_dump(), f, indent=2)
            print(f"✓ Results saved to {args.output}")

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
