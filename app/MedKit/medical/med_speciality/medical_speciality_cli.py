"""medical_speciality.py - Medical Specialists Database and Lookup"""

import json
import sys
import argparse
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

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

    def generate_text(self) -> MedicalSpecialistDatabase:
        """Generate a comprehensive medical specialists database."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.create_user_prompt(),
            response_format=MedicalSpecialistDatabase,
            system_prompt=PromptBuilder.create_system_prompt()
        )

        result = self._ask_llm(model_input)
        return result

    def _ask_llm(self, model_input: ModelInput) -> MedicalSpecialistDatabase:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)

    def print_result(self, database: MedicalSpecialistDatabase) -> None:
        """Print a summary of the generated database using rich."""
        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table
        
        console = Console()
        console.print(Panel(
            f"[bold]Total Specialists:[/bold] {len(database.specialists)}\n"
            f"[bold]Categories:[/bold] {len(database.get_all_categories())}\n"
            f"[bold]Surgical Fields:[/bold] {len(database.get_surgical_specialists())}",
            title="Medical Speciality Database Summary",
            border_style="green"
        ))

        table = Table(title="Specialty Categories")
        table.add_column("Category", style="cyan")
        table.add_column("Count", justify="right", style="magenta")

        categories = {}
        for s in database.specialists:
            cat_name = s.category.name
            categories[cat_name] = categories.get(cat_name, 0) + 1

        for cat, count in categories.items():
            table.add_row(cat, str(count))

        console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive medical specialist database")
    parser.add_argument("-o", "--output", type=Path, help="Path to save JSON output.")
    parser.add_argument("-m", "--model", default="gemini-1.5-pro", help="Model to use (default: gemini-1.5-pro)")

    args = parser.parse_args()

    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        generator = MedicalSpecialityGenerator(model_config=model_config)
        print("Generating medical specialist database...")
        result = generator.generate_text()
        
        generator.print_result(result)
        
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, 'w') as f:
                json.dump(result.model_dump(), f, indent=2)
            print(f"✓ Database saved to {args.output}")

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
