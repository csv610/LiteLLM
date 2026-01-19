"""Module docstring - Drug-Food Interaction Checker.

Analyzes potential interactions between medicines and food/beverage categories with severity
assessment, clinical mechanisms, management recommendations, and patient-friendly guidance
for safe medication-diet coordination.
"""

# ==============================================================================
# STANDARD LIBRARY IMPORTS
# ==============================================================================
import argparse
import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# ==============================================================================
# THIRD-PARTY IMPORTS
# ==============================================================================
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# ==============================================================================
# LOCAL IMPORTS (LiteClient setup)
# ==============================================================================
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

# ==============================================================================
# LOCAL IMPORTS (Module models)
# ==============================================================================
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

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==============================================================================
# CONSTANTS
# ==============================================================================
console = Console()


# ==============================================================================
# CONFIGURATION CLASS
# ==============================================================================

@dataclass
class DrugFoodInteractionConfig:
    """Configuration for drug-food interaction analysis."""
    output_path: Optional[Path] = None
    verbosity: bool = False
    enable_cache: bool = True

# ==============================================================================
# MAIN CLASS
# ==============================================================================

class DrugFoodInteraction:
    """Analyzes drug-food interactions based on provided configuration."""

    def __init__(self, config: DrugFoodInteractionConfig):
        self.config = config
        self.client = LiteClient(
            ModelConfig(model="ollama/gemma3", temperature=0.7)
        )

    def analyze(
        self,
        medicine_name: str,
        diet_type: Optional[str] = None,
        medical_conditions: Optional[str] = None,
        age: Optional[int] = None,
        specific_food: Optional[str] = None,
    ) -> DrugFoodInteractionResult:
        """
        Analyzes how food and beverages interact with a medicine.

        Args:
            medicine_name: Name of the medicine
            diet_type: Patient's diet type (optional)
            medical_conditions: Patient's medical conditions (optional, comma-separated)
            age: Patient's age in years (optional, 0-150)
            specific_food: Specific food(s) to check for interactions (optional, comma-separated)

        Returns:
            DrugFoodInteractionResult: Comprehensive interaction analysis with management recommendations
        """
        # Validate inputs
        if not medicine_name or not medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")
        if age is not None and (age < 0 or age > 150):
            raise ValueError("Age must be between 0 and 150 years")

        logger.info("-" * 80)
        logger.info(f"Starting drug-food interaction analysis")
        logger.info(f"Medicine: {medicine_name}")

        output_path = self.config.output_path
        if output_path is None:
            medicine_clean = medicine_name.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine_clean}_food_interaction.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path}")

        context_parts = [f"Analyzing food interactions for {medicine_name}"]
        if specific_food:
            context_parts.append(f"Specific foods to check: {specific_food}")
            logger.info(f"Specific foods: {specific_food}")
        if diet_type:
            context_parts.append(f"Patient diet type: {diet_type}")
            logger.info(f"Diet type: {diet_type}")
        if age is not None:
            context_parts.append(f"Patient age: {age} years")
            logger.info(f"Patient age: {age}")
        if medical_conditions:
            context_parts.append(f"Patient conditions: {medical_conditions}")
            logger.info(f"Medical conditions: {medical_conditions}")

        context = ". ".join(context_parts) + "."
        logger.debug(f"Context: {context}")

        logger.info("Calling LiteClient.generate_text()...")
        try:
            result = self.client.generate_text(
                model_input=ModelInput(
                    user_prompt=f"{medicine_name} food and beverage interactions analysis. {context}",
                    response_format=DrugFoodInteractionResult,
                )
            )

            logger.info(f"✓ Successfully analyzed food interactions")
            logger.info(f"Overall Severity: {result.interaction_details.overall_severity if result.interaction_details else 'N/A'}")
            logger.info(f"Data Available: {result.data_availability.data_available}")
            logger.info("-" * 80)
            return result
        except Exception as e:
            logger.error(f"✗ Error analyzing food interactions: {e}")
            logger.exception("Full exception details:")
            logger.info("-" * 80)
            raise


def get_drug_food_interaction(
    medicine_name: str,
    config: DrugFoodInteractionConfig,
    diet_type: Optional[str] = None,
    medical_conditions: Optional[str] = None,
    age: Optional[int] = None,
    specific_food: Optional[str] = None,
) -> DrugFoodInteractionResult:
    """
    Get drug-food interaction analysis.

    This is a convenience function that instantiates and runs the
    DrugFoodInteraction analyzer.

    Args:
        medicine_name: Name of the medicine
        config: Configuration object for the analysis
        diet_type: Patient's diet type (optional)
        medical_conditions: Patient's medical conditions (optional)
        age: Patient's age in years (optional)
        specific_food: Specific food(s) to check for interactions (optional)

    Returns:
        DrugFoodInteractionResult: The result of the analysis
    """
    analyzer = DrugFoodInteraction(config)
    return analyzer.analyze(
        medicine_name=medicine_name,
        diet_type=diet_type,
        medical_conditions=medical_conditions,
        age=age,
        specific_food=specific_food,
    )


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================


def get_user_options():
    """
    Get user options through interactive prompts.

    Returns:
        dict: Dictionary containing user-provided options
    """
    print("=" * 80)
    print("DRUG-FOOD INTERACTION CHECKER")
    print("=" * 80 + "\n")

    # Get medicine name (required)
    while True:
        medicine_name = input("Enter medicine name (required): ").strip()
        if medicine_name:
            break
        print("Medicine name cannot be empty. Please try again.\n")

    # Get optional parameters
    diet_type = input("Enter patient's diet type (optional, e.g., vegetarian): ").strip() or None

    age = None
    while True:
        age_input = input("Enter patient's age in years (optional, 0-150): ").strip()
        if not age_input:
            break
        try:
            age = int(age_input)
            if 0 <= age <= 150:
                break
            print("Age must be between 0 and 150. Please try again.\n")
        except ValueError:
            print("Please enter a valid number.\n")

    medical_conditions = input("Enter patient's medical conditions (optional, comma-separated): ").strip() or None

    output_path = input("Enter output file path (optional): ").strip() or None
    output_path = Path(output_path) if output_path else None

    prompt_style_input = input("Enter prompt style (detailed/concise/balanced, default: detailed): ").strip().lower() or "detailed"

    verbose = input("Enable verbose logging? (y/n, default: n): ").strip().lower() == "y"
    json_output = input("Output results as JSON to stdout? (y/n, default: n): ").strip().lower() == "y"

    return {
        "medicine_name": medicine_name,
        "diet_type": diet_type,
        "age": age,
        "medical_conditions": medical_conditions,
        "output_path": output_path,
        "prompt_style": prompt_style_input,
        "verbose": verbose,
        "json_output": json_output,
    }


def create_cli_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser for the CLI.

    Returns:
        argparse.ArgumentParser: Configured parser for command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Drug-Food Interaction Checker - Analyze interactions between medicines and foods",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  python drug_food_interaction.py "Warfarin"

  # With patient details
  python drug_food_interaction.py "Metformin" --age 65 --conditions "kidney disease"

  # With diet type
  python drug_food_interaction.py "Aspirin" --diet-type vegetarian --age 45

  # With custom output
  python drug_food_interaction.py "Simvastatin" --output results.json --verbose
        """,
    )

    # Required arguments
    parser.add_argument(
        "medicine_name",
        type=str,
        help="Name of the medicine to analyze",
    )

    # Optional arguments
    parser.add_argument(
        "--diet-type",
        dest="diet_type",
        type=str,
        default=None,
        help="Patient's diet type (e.g., vegetarian, vegan, kosher)",
    )

    parser.add_argument(
        "--age",
        "-a",
        type=int,
        default=None,
        help="Patient's age in years (0-150)",
    )

    parser.add_argument(
        "--conditions",
        "-c",
        type=str,
        default=None,
        help="Patient's medical conditions (comma-separated)",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output file path for results",
    )

    parser.add_argument(
        "--prompt-style",
        "-p",
        type=str,
        choices=["detailed", "concise", "balanced"],
        default="detailed",
        help="Prompt style for analysis (default: detailed)",
    )

    parser.add_argument(
        "--no-schema",
        action="store_true",
        help="Disable schema-based prompt generation",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Output results as JSON to stdout",
    )

    return parser


# ==============================================================================
# DISPLAY/OUTPUT FUNCTIONS
# ==============================================================================


def print_result(result: DrugFoodInteractionResult, verbose: bool = False) -> None:
    """
    Print interaction analysis results in a formatted manner using rich.

    Args:
        result: The analysis result to print
        verbose: Whether to print detailed information
    """
    console = Console()

    # Print data availability
    if not result.data_availability.data_available:
        console.print(
            Panel(
                f"⚠️  [yellow]{result.data_availability.reason}[/yellow]",
                title="Data Availability",
                border_style="yellow",
            )
        )
        return

    # Print interaction details
    if result.interaction_details:
        details = result.interaction_details

        # Determine severity color
        severity_color = {
            "NONE": "green",
            "MINOR": "blue",
            "MILD": "blue",
            "MODERATE": "yellow",
            "SIGNIFICANT": "yellow",
            "CONTRAINDICATED": "red",
        }.get(details.overall_severity.value, "white")

        # Create details panel
        details_text = (
            f"[bold]Medicine:[/bold] {details.medicine_name}\n"
            f"[bold]Overall Severity:[/bold] [{severity_color}]{details.overall_severity.value}[/{severity_color}]\n"
            f"[bold]Confidence:[/bold] {details.confidence_level.value}\n"
            f"[bold]Data Source:[/bold] {details.data_source_type.value}"
        )

        console.print(
            Panel(
                details_text,
                title="Interaction Details",
                border_style="cyan",
            )
        )

        # Mechanism of interaction
        console.print(
            Panel(
                details.mechanism_of_interaction,
                title="Mechanism of Interaction",
                border_style="blue",
            )
        )

        # Clinical effects
        effects = [effect.strip() for effect in details.clinical_effects.split(",")]
        console.print("[bold cyan]Clinical Effects:[/bold cyan]")
        for effect in effects:
            console.print(f"  • {effect}")
        console.print()

        # Foods to avoid
        foods_avoid = [food.strip() for food in details.foods_to_avoid.split(",")]
        console.print("[bold red]Foods to Avoid:[/bold red]")
        for food in foods_avoid:
            console.print(f"  • {food}")
        console.print()

        # Safe foods
        foods_safe = [food.strip() for food in details.foods_safe_to_consume.split(",")]
        console.print("[bold green]Foods Safe to Consume:[/bold green]")
        for food in foods_safe:
            console.print(f"  • {food}")
        console.print()

        # Management recommendations
        recommendations = [rec.strip() for rec in details.management_recommendations.split(",")]
        console.print("[bold cyan]Management Recommendations:[/bold cyan]")
        for rec in recommendations:
            console.print(f"  • {rec}")
        console.print()

        # Print detailed category interactions if verbose
        if verbose:
            console.print("[bold yellow]Detailed Category Interactions:[/bold yellow]")
            for interaction in details.food_category_interactions:
                if interaction.has_interaction:
                    cat_text = f"[bold]{interaction.category.value}[/bold]\n"
                    cat_text += f"  Severity: {interaction.severity.value}\n"
                    cat_text += f"  Foods: {interaction.specific_foods}"
                    if interaction.mechanism:
                        cat_text += f"\n  Mechanism: {interaction.mechanism}"
                    if interaction.timing_recommendation:
                        cat_text += f"\n  Timing: {interaction.timing_recommendation}"
                    console.print(cat_text)
            console.print()

    # Print patient-friendly summary
    if result.patient_friendly_summary:
        summary = result.patient_friendly_summary

        # Simple explanation
        console.print(
            Panel(
                summary.simple_explanation,
                title="Simple Explanation",
                border_style="green",
            )
        )

        # What patient should do
        console.print(
            Panel(
                summary.what_patient_should_do,
                title="What You Should Do",
                border_style="green",
            )
        )

        # Meal timing guidance
        console.print(
            Panel(
                summary.meal_timing_guidance,
                title="Meal Timing Guidance",
                border_style="blue",
            )
        )

        # Warning signs
        warning_signs = [sign.strip() for sign in summary.warning_signs.split(",")]
        console.print("[bold yellow]Warning Signs:[/bold yellow]")
        for sign in warning_signs:
            console.print(f"  • {sign}")
        console.print()

    # Print technical summary
    console.print(
        Panel(
            result.technical_summary,
            title="Technical Summary",
            border_style="magenta",
        )
    )


# ==============================================================================
# ARGUMENT PARSER
# ==============================================================================


# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main() -> int:
    """
    Main entry point for the drug-food interaction CLI.

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    parser = create_cli_parser()
    args = parser.parse_args()

    # Configure logging verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    try:
        # Create configuration
        config = DrugFoodInteractionConfig(
            output_path=args.output if hasattr(args, 'output') else None,
            verbosity=args.verbose if hasattr(args, 'verbose') else False,
        )

        logger.info(f"Configuration created successfully")

        # Run analysis
        analyzer = DrugFoodInteraction(config)
        result = analyzer.analyze(
            medicine_name=args.medicine_name,
            diet_type=args.diet_type if hasattr(args, 'diet_type') else None,
            medical_conditions=args.conditions if hasattr(args, 'conditions') else None,
            age=args.age if hasattr(args, 'age') else None,
            specific_food=None,
        )

        # Print results
        print_result(result, verbose=args.verbose)

        # Save results to file
        if args.output:
            output_path = args.output
        else:
            medicine_clean = args.medicine_name.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine_clean}_food_interaction.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            f.write(result.model_dump_json(indent=2))

        logger.info(f"✓ Results saved to {output_path}")
        print(f"\n✓ Results saved to: {output_path}")

        # Output JSON to stdout if requested
        if args.json_output:
            print(f"\n{result.model_dump_json(indent=2)}")

        return 0

    except ValueError as e:
        print(f"\n❌ Invalid input: {e}", file=sys.stderr)
        logger.error(f"Invalid input: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        logger.error(f"Unexpected error: {e}")
        logger.exception("Full exception details:")
        return 1


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    sys.exit(main())
