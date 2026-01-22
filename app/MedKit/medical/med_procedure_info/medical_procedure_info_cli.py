"""medical_procedure_info - Generate comprehensive medical procedure documentation."""

import json
import sys
import argparse
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

from medical_procedure_info_models import ProcedureInfo


class PromptBuilder:
    """Builder class for creating prompts for medical procedure documentation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for medical procedure documentation."""
        return "You are an expert medical documentation specialist. Generate comprehensive, evidence-based procedure information."

    @staticmethod
    def create_user_prompt(procedure: str) -> str:
        """Create the user prompt for procedure information."""
        return f"Generate complete, evidence-based information for the medical procedure: {procedure}"


class MedicalProcedureInfoGenerator:
    """Generate comprehensive information for medical procedures using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.client = LiteClient(model_config=model_config)
        self.procedure_name: Optional[str] = None

    def generate_text(self, procedure: str) -> ProcedureInfo:
        """Generate and retrieve comprehensive medical procedure information."""
        if not procedure or not procedure.strip():
            raise ValueError("Procedure name cannot be empty")

        self.procedure_name = procedure

        model_input = ModelInput(
            user_prompt=PromptBuilder.create_user_prompt(procedure),
            response_format=ProcedureInfo,
            system_prompt=PromptBuilder.create_system_prompt()
        )

        result = self._ask_llm(model_input)
        return result

    def _ask_llm(self, model_input: ModelInput) -> ProcedureInfo:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)

    def print_result(self, info: ProcedureInfo) -> None:
        """Print a summary of the generated procedure information using rich."""
        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table
        
        console = Console()
        console.print(Panel(
            f"[bold]Procedure:[/bold] {info.metadata.procedure_name}\n"
            f"[bold]Category:[/bold] {info.metadata.procedure_category}\n"
            f"[bold]Specialty:[/bold] {info.metadata.medical_specialty}\n\n"
            f"[bold]Purpose:[/bold] {info.purpose.primary_purpose}",
            title="Medical Procedure Documentation",
            border_style="blue"
        ))

        table = Table(title="Procedure Highlights")
        table.add_column("Section", style="cyan")
        table.add_column("Key Information", style="white")

        table.add_row("Indications", info.indications.when_recommended[:100] + "...")
        table.add_row("Preparation", info.preparation.fasting_required)
        table.add_row("Anesthesia", info.details.anesthesia_type)
        table.add_row("Recovery", info.recovery.recovery_timeline)
        table.add_row("Success Rate", info.outcomes.success_rate)
        
        console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive information for a medical procedure.")
    parser.add_argument("-i", "--procedure", required=True, help="Name of the medical procedure")
    parser.add_argument("-o", "--output", type=Path, help="Path to save JSON output.")
    parser.add_argument("-m", "--model", default="gemini-1.5-pro", help="Model to use (default: gemini-1.5-pro)")

    args = parser.parse_args()

    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        generator = MedicalProcedureInfoGenerator(model_config=model_config)
        print(f"Generating procedure documentation for: {args.procedure}...")
        result = generator.generate_text(procedure=args.procedure)
        
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
