import argparse
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging

from drug_drug_interaction_models import (
    DrugInteractionSeverity,
    ConfidenceLevel,
    DataSourceType,
    DrugInteractionDetails,
    PatientFriendlySummary,
    DataAvailabilityInfo,
    DrugInteractionResult,
)

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for creating prompts for drug-drug interaction analysis."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for drug-drug interaction analysis.

        Returns:
            str: System prompt defining the AI's role and instructions
        """
        return """You are a clinical pharmacology expert specializing in drug-drug interactions. Your role is to analyze how medications interact with each other, affecting their efficacy, safety, and metabolism.

When analyzing drug-drug interactions, you must:

1. Identify potential pharmacokinetic interactions (absorption, distribution, metabolism, excretion)
2. Identify potential pharmacodynamic interactions (additive, synergistic, or antagonistic effects)
3. Assess the severity and clinical significance of each interaction
4. Explain the mechanism of interaction clearly
5. Evaluate the risk level and potential adverse effects
6. Provide specific management recommendations and monitoring parameters
7. Consider patient-specific factors such as age, dosage, and medical conditions
8. Base analysis on established medical literature, clinical guidelines, and drug interaction databases

Always prioritize patient safety while providing practical, evidence-based guidance for medication management."""

    @staticmethod
    def create_user_prompt(medicine1: str, medicine2: str, context: str) -> str:
        """
        Create the user prompt for drug-drug interaction analysis.

        Args:
            medicine1: The name of the first medicine
            medicine2: The name of the second medicine
            context: Additional context for the analysis

        Returns:
            str: Formatted user prompt
        """
        return f"{medicine1} and {medicine2} interaction analysis. {context}"


@dataclass
class DrugDrugInput:
    """Configuration and input for drug-drug interaction analysis."""
    medicine1: str
    medicine2: str
    age: Optional[int] = None
    dosage1: Optional[str] = None
    dosage2: Optional[str] = None
    medical_conditions: Optional[str] = None
    prompt_style: str = "detailed"

class DrugDrugInteraction:
    """Analyzes drug-drug interactions based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def generate_text(self, config: DrugDrugInput) -> DrugInteractionResult:
        """Analyzes how two drugs interact."""
        self._validate_input(config)

        logger.info("-" * 80)
        logger.info(f"Starting drug-drug interaction analysis")
        logger.info(f"Drug 1: {config.medicine1}")
        logger.info(f"Drug 2: {config.medicine2}")

        context = self._prepare_context(config)
        logger.debug(f"Context: {context}")

        user_prompt = self._create_prompt(config, context)
        model_input = self._create_model_input(user_prompt)
        result = self._ask_llm(model_input)

        logger.info(f"✓ Successfully analyzed interaction")
        logger.info(f"Severity: {result.interaction_details.severity_level if result.interaction_details else 'N/A'}")
        logger.info(f"Data Available: {result.data_availability.data_available}")
        logger.info("-" * 80)
        return result

    def _validate_input(self, config: DrugDrugInput) -> None:
        """Validate input parameters."""
        if not config.medicine1 or not config.medicine1.strip():
            raise ValueError("Medicine 1 name cannot be empty")
        if not config.medicine2 or not config.medicine2.strip():
            raise ValueError("Medicine 2 name cannot be empty")
        if config.age is not None and (config.age < 0 or config.age > 150):
            raise ValueError("Age must be between 0 and 150 years")

    def _prepare_context(self, config: DrugDrugInput) -> str:
        """Build the analysis context string from input parameters."""
        context_parts = [f"Checking interaction between {config.medicine1} and {config.medicine2}"]
        
        if config.age is not None:
            context_parts.append(f"Patient age: {config.age} years")
        if config.dosage1:
            context_parts.append(f"{config.medicine1} dosage: {config.dosage1}")
        if config.dosage2:
            context_parts.append(f"{config.medicine2} dosage: {config.dosage2}")
        if config.medical_conditions:
            context_parts.append(f"Patient conditions: {config.medical_conditions}")

        return ". ".join(context_parts) + "."

    def _create_prompt(self, config: DrugDrugInput, context: str) -> str:
        """Create the user prompt for the LLM."""
        return PromptBuilder.create_user_prompt(config.medicine1, config.medicine2, context)

    def _create_model_input(self, user_prompt: str) -> ModelInput:
        """Create the ModelInput for the LiteClient."""
        return ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=user_prompt,
            response_format=DrugInteractionResult,
        )

    def _ask_llm(self, model_input: ModelInput) -> DrugInteractionResult:
        """Helper to call LiteClient with error handling."""
        logger.info("Calling LiteClient.generate_text()...")
        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"✗ Error during drug interaction analysis: {e}")
            logger.exception("Full exception details:")
            raise

def get_user_arguments():
    """Create and configure the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Drug-Drug Interaction Analyzer - Check interactions between two medicines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=\"\"\"
Examples:
  python drug_drug_interaction.py "Warfarin" "Aspirin"
  python drug_drug_interaction.py "Metformin" "Lisinopril" --age 65 --dosage1 "500mg twice daily"
  python drug_drug_interaction.py "Simvastatin" "Clarithromycin" --prompt-style detailed --verbose
        \"\"\",
    )

    parser.add_argument("medicine1", type=str, help="Name of the first medicine")
    parser.add_argument("medicine2", type=str, help="Name of the second medicine")
    parser.add_argument("--age", "-a", type=int, default=None, help="Patient's age in years (0-150)")
    parser.add_argument("--dosage1", "-d1", type=str, default=None, help="Dosage information for first medicine")
    parser.add_argument("--dosage2", "-d2", type=str, default=None, help="Dosage information for second medicine")
    parser.add_argument("--conditions", "-c", type=str, default=None, help="Patient's medical conditions (comma-separated)")
    parser.add_argument("--prompt-style", "-p", type=str, choices=["detailed", "concise", "balanced"], default="detailed", help="Prompt style for analysis (default: detailed)")
    parser.add_argument("--no-schema", action="store_true", default=False, help="Disable schema-based prompt generation")
    parser.add_argument("--verbosity", "-v", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2)")
    parser.add_argument("--model", "-m", type=str, default="ollama/gemma3", help="Model ID to use for analysis (default: ollama/gemma3)")
    parser.add_argument("--json-output", "-j", action="store_true", default=False, help="Output results as JSON to stdout")

    return parser.parse_args()

def print_result(result: DrugInteractionResult, verbose: bool = False) -> None:
    """Print interaction analysis results in a formatted manner using rich."""
    console = Console()
    console.print()

    if not result.data_availability.data_available:
        console.print(
            Panel(
                f"⚠️  [yellow]{result.data_availability.reason}[/yellow]",
                title="Data Availability",
                border_style="yellow",
            )
        )
        return

    if result.interaction_details:
        details = result.interaction_details
        severity_color = {
            "NONE": "green",
            "MINOR": "blue",
            "SIGNIFICANT": "yellow",
            "CONTRAINDICATED": "red",
        }.get(details.severity_level.value, "white")

        details_text = (
            f"[bold]Drug 1:[/bold] {details.drug1_name}\n"
            f"[bold]Drug 2:[/bold] {details.drug2_name}\n"
            f"[bold]Severity:[/bold] [{severity_color}]{details.severity_level.value}[/{severity_color}]\n"
            f"[bold]Confidence:[/bold] {details.confidence_level.value}\n"
            f"[bold]Data Source:[/bold] {details.data_source_type.value}"
        )

        console.print(Panel(details_text, title="Drug Interaction Details", border_style="cyan"))

        console.print(Panel(details.mechanism_of_interaction, title="Mechanism of Interaction", border_style="blue"))

        effects = [effect.strip() for effect in details.clinical_effects.split(",")]
        console.print("[bold cyan]Clinical Effects:[/bold cyan]")
        for effect in effects:
            console.print(f"  • {effect}")
        console.print()

        recommendations = [rec.strip() for rec in details.management_recommendations.split(",")]
        console.print("[bold cyan]Management Recommendations:[/bold cyan]")
        for rec in recommendations:
            console.print(f"  • {rec}")
        console.print()

        alternatives = [alt.strip() for alt in details.alternative_medicines.split(",")]
        console.print("[bold cyan]Alternative Medicines:[/bold cyan]")
        for alt in alternatives:
            console.print(f"  • {alt}")
        console.print()

    if result.patient_friendly_summary:
        summary = result.patient_friendly_summary
        console.print(Panel(summary.simple_explanation, title="Simple Explanation", border_style="green"))
        console.print(Panel(summary.what_patient_should_do, title="What You Should Do", border_style="green"))

        warning_signs = [sign.strip() for sign in summary.warning_signs.split(",")]
        console.print("[bold yellow]Warning Signs:[/bold yellow]")
        for sign in warning_signs:
            console.print(f"  • {sign}")
        console.print()

        console.print(Panel(summary.when_to_seek_help, title="When to Seek Help", border_style="red"))

    console.print(Panel(result.technical_summary, title="Technical Summary", border_style="magenta"))
    console.print()

def app_cli():
    """Main entry point for the drug-drug interaction CLI."""
    console = Console()
    args = get_user_arguments()

    configure_logging(
        log_file="drug_drug_interaction.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    try:
        config = DrugDrugInput(
            medicine1=args.medicine1,
            medicine2=args.medicine2,
            age=args.age,
            dosage1=args.dosage1,
            dosage2=args.dosage2,
            medical_conditions=args.conditions,
            prompt_style=args.prompt_style,
        )

        logger.info(f"Configuration created successfully")

        model_config = ModelConfig(model=args.model, temperature=0.7)
        analyzer = DrugDrugInteraction(model_config)
        result = analyzer.generate_text(config)

        print_result(result, verbose=args.verbosity >= 3)

        if args.json_output:
            console.print(f"\n{result.model_dump_json(indent=2)}")

        return 0

    except ValueError as e:
        console.print(f"\n❌ [red]Invalid input:[/red] {e}")
        logger.error(f"Invalid input: {e}")
        return 1
    except Exception as e:
        console.print(f"\n❌ [red]Error:[/red] {e}")
        logger.error(f"Unexpected error: {e}")
        logger.exception("Full exception details:")
        return 1

if __name__ == "__main__":
    sys.exit(app_cli())
