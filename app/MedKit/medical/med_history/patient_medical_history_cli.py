"""patient_medical_history_cli.py - Generate exam-specific medical history questions."""

import json
import sys
import argparse
from pathlib import Path
from typing import Union

from dataclasses import dataclass, field

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from patient_medical_history_models import PatientMedicalHistoryModel, ModelOutput

@dataclass
class MedicalHistoryInput:
    exam: str
    age: int
    gender: str
    purpose: str = "physical_exam"

class PromptBuilder:
    """Builder class for creating prompts for patient medical history questions."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for medical history question generation.
        
        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return "You are an expert medical documentation specialist. Generate trauma-informed, clinically relevant medical history questions."

    @staticmethod
    def create_user_prompt(medical_history_input: MedicalHistoryInput) -> str:
        """Create the user prompt for medical history question generation.
        
        Args:
            medical_history_input: Input parameters for medical history generation
            
        Returns:
            str: Formatted user prompt
        """
        return f"""Generate comprehensive medical history questions for a {medical_history_input.age}-year-old {medical_history_input.gender} patient undergoing a {medical_history_input.exam} exam for the purpose of {medical_history_input.purpose}.

The questions should be:
1. Trauma-informed: Respectful, non-judgmental, and culturally sensitive.
2. Purpose-specific: 
   - 'surgery': Focus on anesthesia risk, bleeding, and recovery.
   - 'medication': Focus on allergies, interactions, and adherence.
   - 'physical_exam': Focus on current status and systematic review.
3. Clinically relevant: Explain why each question matters for the {medical_history_input.exam} exam.
4. Comprehensive: Include past history, family history, drug info, vaccinations, and lifestyle/social factors.

Provide follow-up questions for positive responses to key clinical indicators."""


class PatientMedicalHistoryGenerator:
    """Generates patient medical history questions using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.client = LiteClient(model_config=model_config)

    def generate_text(self, user_input: MedicalHistoryInput, structured: bool = False) -> ModelOutput:
        """Generate patient medical history questions."""

        response_format = None
        if structured:
            response_format = PatientMedicalHistoryModel

        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(medical_history_input),
            response_format=response_format,
        )

        result = self._ask_llm(model_input)

        # Ensure input params are mirrored in result
#        result.purpose = medical_history_input.purpose
#        result.exam = medical_history_input.exam
#        result.age = medical_history_input.age
#        result.gender = medical_history_input.gender

        return result

    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)


def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive patient medical history questions.")
    parser.add_argument("-e", "--exam", required=True, help="Type of medical exam (e.g., cardiac, respiratory)")
    parser.add_argument("-a", "--age", type=int, required=True, help="Patient age in years")
    parser.add_argument("-g", "--gender", required=True, help="Patient gender")
    parser.add_argument("-o", "--output", type=Path, help="Path to save JSON output.")
    parser.add_argument("-m", "--model", default="gemini-1.5-pro", help="Model to use (default: gemini-1.5-pro)")
    parser.add_argument("-s", "--structured", action="store_true", default=False, help="Use structured output (Pydantic model) for the response.")

    args = parser.parse_args()

    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        generator = PatientMedicalHistoryGenerator(model_config=model_config)
        print(f"Generating medical history questions for {args.exam} ({args.purpose})...")
        medical_history_input = MedicalHistoryInput(
            exam=args.exam,
            age=args.age,
            gender=args.gender,
            purpose=args.purpose
        )
        result = generator.generate_text(medical_history_input, structured=args.structured)
        
        if args.output:
            output_path = args.output
            if isinstance(result, str) and output_path.suffix == ".json":
                output_path = output_path.with_suffix(".md")
            save_model_response(result, output_path)
            print(f"✓ Results saved to {output_path}")

    except ValueError as e:
        print(f"✗ Validation error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
