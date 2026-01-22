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

from drug_food_interaction_models import (
    FoodCategory,
    InteractionSeverity,
    ConfidenceLevel,
    DataSourceType,
    FoodCategoryInteraction,
    DrugFoodInteractionDetails,
    PatientFriendlySummary,
    DataAvailabilityInfo,
    DrugFoodInteractionResult,
)

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for creating prompts for drug-food interaction analysis."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for drug-food interaction analysis.

        Returns:
            str: System prompt defining the AI's role and instructions
        """
        return """You are a clinical pharmacology expert specializing in drug-food interactions. Your role is to analyze how foods and beverages affect drug absorption, metabolism, efficacy, and safety.

When analyzing drug-food interactions, you must:

1. Identify significant food interactions that affect drug absorption, distribution, metabolism, or excretion
2. Assess the severity and clinical significance of each interaction
3. Provide specific guidance on which foods to avoid and which are safe to consume
4. Explain the mechanism of interaction in clear terms
5. Recommend optimal timing for medication administration relative to meals
6. Highlight any special dietary considerations or restrictions
7. Base analysis on established medical literature and clinical guidelines

Always prioritize patient safety while providing practical, evidence-based guidance for optimal medication use."""

    @staticmethod
    def create_user_prompt(medicine_name: str, context: str) -> str:
        """
        Create the user prompt for drug-food interaction analysis.

        Args:
            medicine_name: The name of the medicine to analyze
            context: Additional context for the analysis

        Returns:
            str: Formatted user prompt
        """
        return f"{medicine_name} food and beverage interactions analysis. {context}"


@dataclass
class DrugFoodInput:
    """Configuration and input for drug-food interaction analysis."""
    medicine_name: str
    diet_type: Optional[str] = None
    medical_conditions: Optional[str] = None
    age: Optional[int] = None
    specific_food: Optional[str] = None
    prompt_style: str = "detailed"

class DrugFoodInteraction:
    """Analyzes drug-food interactions based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def generate_text(self, config: DrugFoodInput) -> DrugFoodInteractionResult:
        """Analyzes how food and beverages interact with a medicine."""
        self._validate_input(config)

        logger.info("-" * 80)
        logger.info(f"Starting drug-food interaction analysis")
        logger.info(f"Medicine: {config.medicine_name}")

        context = self._prepare_context(config)
        logger.debug(f"Context: {context}")

        user_prompt = self._create_prompt(config, context)
        model_input = self._create_model_input(user_prompt)
        result = self._ask_llm(model_input)

        logger.info(f"✓ Successfully analyzed food interactions")
        logger.info(f"Overall Severity: {result.interaction_details.overall_severity if result.interaction_details else 'N/A'}")
        logger.info(f"Data Available: {result.data_availability.data_available}")
        logger.info("-" * 80)
        return result

    def _validate_input(self, config: DrugFoodInput) -> None:
        """Validate input parameters."""
        if not config.medicine_name or not config.medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")
        if config.age is not None and (config.age < 0 or config.age > 150):
            raise ValueError("Age must be between 0 and 150 years")

    def _prepare_context(self, config: DrugFoodInput) -> str:
        """Build the analysis context string from input parameters."""
        context_parts = [f"Analyzing food interactions for {config.medicine_name}"]
        if config.specific_food:
            context_parts.append(f"Specific foods to check: {config.specific_food}")
        if config.diet_type:
            context_parts.append(f"Patient diet type: {config.diet_type}")
        if config.age is not None:
            context_parts.append(f"Patient age: {config.age} years")
        if config.medical_conditions:
            context_parts.append(f"Patient conditions: {config.medical_conditions}")
        return ". ".join(context_parts) + "."

    def _create_prompt(self, config: DrugFoodInput, context: str) -> str:
        """Create the user prompt for the LLM."""
        return PromptBuilder.create_user_prompt(config.medicine_name, context)

    def _create_model_input(self, user_prompt: str) -> ModelInput:
        """Create the ModelInput for the LiteClient."""
        return ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=user_prompt,
            response_format=DrugFoodInteractionResult,
        )

    def _ask_llm(self, model_input: ModelInput) -> DrugFoodInteractionResult:
        """Helper to call LiteClient with error handling."""
        logger.info("Calling LiteClient.generate_text()...")
        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"✗ Error during LLM analysis: {e}")
            logger.exception("Full exception details:")
            raise

def get_user_arguments():
    """Create and configure the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Drug-Food Interaction Checker - Analyze interactions between medicines and foods",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=\"\"\"
Examples:
  python drug_food_interaction.py "Warfarin"
  python drug_food_interaction.py "Metformin" --age 65 --conditions "kidney disease"
  python drug_food_interaction.py "Simvastatin" --verbose
        \"\"\",
    )

    parser.add_argument("medicine_name", type=str, help="Name of the medicine to analyze")
    parser.add_argument("--diet-type", type=str, default=None, help="Patient's diet type")
    parser.add_argument("--age", "-a", type=int, default=None, help="Patient's age in years (0-150)")
    parser.add_argument("--conditions", "-c", type=str, default=None, help="Patient's medical conditions")
    parser.add_argument("--prompt-style", "-p", type=str, choices=["detailed", "concise", "balanced"], default="detailed", help="Prompt style")
    parser.add_argument("--no-schema", action="store_true", help="Disable schema-based prompt generation")
    parser.add_argument("--verbosity", "-v", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Logging verbosity level")
    parser.add_argument("--model", "-m", type=str, default="ollama/gemma3", help="Model ID")
    parser.add_argument("--json-output", action="store_true", help="Output results as JSON to stdout")

    return parser.parse_args()

def print_result(result: DrugFoodInteractionResult, verbose: bool = False) -> None:
    """Print interaction analysis results in a formatted manner using rich."""
    console = Console()
    console.print()

    if not result.data_availability.data_available:
        console.print(Panel(f"⚠️  [yellow]{result.data_availability.reason}[/yellow]", title="Data Availability", border_style="yellow"))
        return

    if result.interaction_details:
        details = result.interaction_details
        severity_color = {
            "NONE": "green", "MINOR": "blue", "MILD": "blue", "MODERATE": "yellow", "SIGNIFICANT": "yellow", "CONTRAINDICATED": "red"
        }.get(details.overall_severity.value, "white")

        details_text = (
            f"[bold]Medicine:[/bold] {details.medicine_name}\n"
            f"[bold]Overall Severity:[/bold] [{severity_color}]{details.overall_severity.value}[/{severity_color}]\n"
            f"[bold]Confidence:[/bold] {details.confidence_level.value}\n"
            f"[bold]Data Source:[/bold] {details.data_source_type.value}"
        )

        console.print(Panel(details_text, title="Interaction Details", border_style="cyan"))
        console.print(Panel(details.mechanism_of_interaction, title="Mechanism of Interaction", border_style="blue"))

        effects = [effect.strip() for effect in details.clinical_effects.split(",")]
        console.print("[bold cyan]Clinical Effects:[/bold cyan]")
        for effect in effects:
            console.print(f"  • {effect}")
        console.print()

        foods_avoid = [food.strip() for food in details.foods_to_avoid.split(",")]
        console.print("[bold red]Foods to Avoid:[/bold red]")
        for food in foods_avoid:
            console.print(f"  • {food}")
        console.print()

        foods_safe = [food.strip() for food in details.foods_safe_to_consume.split(",")]
        console.print("[bold green]Foods Safe to Consume:[/bold green]")
        for food in foods_safe:
            console.print(f"  • {food}")
        console.print()

        recommendations = [rec.strip() for rec in details.management_recommendations.split(",")]
        console.print("[bold cyan]Management Recommendations:[/bold cyan]")
        for rec in recommendations:
            console.print(f"  • {rec}")
        console.print()

        if verbose:
            console.print("[bold yellow]Detailed Category Interactions:[/bold yellow]")
            for interaction in details.food_category_interactions:
                if interaction.has_interaction:
                    cat_text = f"[bold]{interaction.category.value}[/bold]\n  Severity: {interaction.severity.value}\n  Foods: {interaction.specific_foods}"
                    if interaction.mechanism: cat_text += f"\n  Mechanism: {interaction.mechanism}"
                    if interaction.timing_recommendation: cat_text += f"\n  Timing: {interaction.timing_recommendation}"
                    console.print(cat_text)
            console.print()

    if result.patient_friendly_summary:
        summary = result.patient_friendly_summary
        console.print(Panel(summary.simple_explanation, title="Simple Explanation", border_style="green"))
        console.print(Panel(summary.what_patient_should_do, title="What You Should Do", border_style="green"))
        console.print(Panel(summary.meal_timing_guidance, title="Meal Timing Guidance", border_style="blue"))

        warning_signs = [sign.strip() for sign in summary.warning_signs.split(",")]
        console.print("[bold yellow]Warning Signs:[/bold yellow]")
        for sign in warning_signs:
            console.print(f"  • {sign}")
        console.print()

    console.print(Panel(result.technical_summary, title="Technical Summary", border_style="magenta"))
    console.print()

def main() -> int:
    """Main entry point for the drug-food interaction CLI."""
    console = Console()
    args = get_user_arguments()

    configure_logging(
        log_file="drug_food_interaction.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    try:
        config = DrugFoodInput(
            medicine_name=args.medicine_name,
            diet_type=args.diet_type,
            medical_conditions=args.conditions,
            age=args.age,
            specific_food=None,
            prompt_style=args.prompt_style,
        )

        logger.info(f"Configuration created successfully")

        model_config = ModelConfig(model=args.model, temperature=0.7)
        analyzer = DrugFoodInteraction(model_config)
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
    sys.exit(main())


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    sys.exit(main())
