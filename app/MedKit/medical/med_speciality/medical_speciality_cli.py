"""medical_speciality.py - Medical Specialists Database and Lookup"""

import json
import sys
import argparse
from pathlib import Path
from typing import Optional, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response
from utils.output_formatter import print_result

from medical_speciality_models import MedicalSpecialistDatabase


class PromptBuilder:
    """Builder class for creating prompts for medical speciality generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Generate the system prompt for the medical specialties generator."""
        return "You are an expert in medical education and healthcare systems. Generate a complete and accurate database of medical specialties."

    @staticmethod
    def create_user_prompt() -> str:
        """Generate the user prompt for the medical specialties generator."""
        return """Generate a comprehensive list of medical specialists covering all major fields of medicine.
Organize them by logical categories (body system, type of care, patient population).

For each specialist, provide:
1. Formal specialty name
2. Category name and description
3. Role description
4. Conditions/diseases treated
5. Common referral reasons
6. Subspecialties
7. Surgical vs non-surgical
8. Patient population focus

Include both common (cardiology, dermatology) and specialized (physiatry, interventional radiology) fields."""


class MedicalSpecialityGenerator:
    """Generate a comprehensive database of medical specialities using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.client = LiteClient(model_config=model_config)

    def generate_text(self, structured: bool = False) -> Union[MedicalSpecialistDatabase, str]:
        """Generate a comprehensive medical specialists database."""
        response_format = None
        if structured:
            response_format = MedicalSpecialistDatabase

        model_input = ModelInput(
            user_prompt=PromptBuilder.create_user_prompt(),
            response_format=response_format,
            system_prompt=PromptBuilder.create_system_prompt()
        )

        result = self._ask_llm(model_input)
        return result

    def _ask_llm(self, model_input: ModelInput) -> Union[MedicalSpecialistDatabase, str]:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)


def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive medical specialist database")
    parser.add_argument("-o", "--output", type=Path, help="Path to save JSON output.")
    parser.add_argument("-m", "--model", default="gemini-1.5-pro", help="Model to use (default: gemini-1.5-pro)")
    parser.add_argument("-s", "--structured", action="store_true", default=False, help="Use structured output (Pydantic model) for the response.")

    args = parser.parse_args()

    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        generator = MedicalSpecialityGenerator(model_config=model_config)
        print("Generating medical specialist database...")
        result = generator.generate_text(structured=args.structured)
        
        print_result(result, title="Medical Speciality Database")
        
        if args.output:
            output_path = args.output
            if isinstance(result, str) and output_path.suffix == ".json":
                output_path = output_path.with_suffix(".md")
            save_model_response(result, output_path)
            print(f"✓ Database saved to {output_path}")

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
