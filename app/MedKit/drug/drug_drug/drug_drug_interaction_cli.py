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
console = Console()

@dataclass
class DrugDrugInput:
    """Configuration and input for drug-drug interaction analysis."""
    medicine1: str
    medicine2: str
    age: Optional[int] = None
    dosage1: Optional[str] = None
    dosage2: Optional[str] = None
    medical_conditions: Optional[str] = None
    output_path: Optional[Path] = None
    prompt_style: str = "detailed"


# ==============================================================================
# MAIN CLASS
# ==============================================================================

class DrugDrugInteraction:
    """Analyzes drug-drug interactions based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def _validate_input(self, config: DrugDrugInput) -> None:
        """Validate input parameters."""
        if not config.medicine1 or not config.medicine1.strip():
            raise ValueError("Medicine 1 name cannot be empty")
        if not config.medicine2 or not config.medicine2.strip():
            raise ValueError("Medicine 2 name cannot be empty")
        if config.age is not None and (config.age < 0 or config.age > 150):
            raise ValueError("Age must be between 0 and 150 years")

    def _get_output_path(self, config: DrugDrugInput) -> Path:
        """Determine the file path for saving analysis results."""
        if config.output_path:
            return config.output_path
        
        medicine1_clean = config.medicine1.lower().replace(' ', '_')
        medicine2_clean = config.medicine2.lower().replace(' ', '_')
        return Path("outputs") / f"{medicine1_clean}_{medicine2_clean}_interaction.json"

    def _prepare_context(self, config: DrugDrugInput) -> str:
        """Build the analysis context string from input parameters."""
        context_parts = [f"Checking interaction between {config.medicine1} and {config.medicine2}"]
        
        if config.age is not None:
            context_parts.append(f"Patient age: {config.age} years")
            logger.info(f"Patient age: {config.age}")
        if config.dosage1:
            context_parts.append(f"{config.medicine1} dosage: {config.dosage1}")
            logger.info(f"{config.medicine1} dosage: {config.dosage1}")
        if config.dosage2:
            context_parts.append(f"{config.medicine2} dosage: {config.dosage2}")
            logger.info(f"{config.medicine2} dosage: {config.dosage2}")
        if config.medical_conditions:
            context_parts.append(f"Patient conditions: {config.medical_conditions}")
            logger.info(f"Medical conditions: {config.medical_conditions}")

        return ". ".join(context_parts) + "."

    def _execute_llm_analysis(self, config: DrugDrugInput, context: str) -> DrugInteractionResult:
        """Call LiteClient to perform the interaction analysis."""
        logger.info("Calling LiteClient.generate_text()...")
        try:
            return self.client.generate_text(
                model_input=ModelInput(
                    user_prompt=f"{config.medicine1} and {config.medicine2} interaction analysis. {context}",
                    response_format=DrugInteractionResult,
                )
            )
        except Exception as e:
            logger.error(f"✗ Error analyzing drug interaction: {e}")
            logger.exception("Full exception details:")
            raise

    def analyze(self, config: DrugDrugInput) -> DrugInteractionResult:
        """
        Analyzes how two drugs interact.

        Args:
            config: Configuration and input for analysis

        Returns:
            DrugInteractionResult: Comprehensive interaction analysis with management recommendations
        """
        self._validate_input(config)

        logger.info("-" * 80)
        logger.info(f"Starting drug-drug interaction analysis")
        logger.info(f"Drug 1: {config.medicine1}")
        logger.info(f"Drug 2: {config.medicine2}")

        output_path = self._get_output_path(config)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path}")

        context = self._prepare_context(config)
        logger.debug(f"Context: {context}")

        result = self._execute_llm_analysis(config, context)

        logger.info(f"✓ Successfully analyzed interaction")
        logger.info(f"Severity: {result.interaction_details.severity_level if result.interaction_details else 'N/A'}")
        logger.info(f"Data Available: {result.data_availability.data_available}")
        logger.info("-" * 80)
        return result



def get_user_arguments():
    """
    Create and configure the argument parser for the CLI.

    Returns:
        argparse.ArgumentParser: Configured parser for command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Drug-Drug Interaction Analyzer - Check interactions between two medicines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  python drug_drug_interaction.py "Warfarin" "Aspirin"

  # With patient details
  python drug_drug_interaction.py "Metformin" "Lisinopril" --age 65 --dosage1 "500mg twice daily"

  # With medical conditions and custom output
  python drug_drug_interaction.py "Ibuprofen" "Aspirin" --conditions "hypertension, diabetes" --output interaction.json

  # With detailed prompt style
  python drug_drug_interaction.py "Simvastatin" "Clarithromycin" --prompt-style detailed --verbose
        """,
    )

    # Required arguments
    parser.add_argument(
        "medicine1",
        type=str,
        help="Name of the first medicine",
    )

    parser.add_argument(
        "medicine2",
        type=str,
        help="Name of the second medicine",
    )

    # Optional arguments
    parser.add_argument(
        "--age",
        "-a",
        type=int,
        default=None,
        help="Patient's age in years (0-150)",
    )

    parser.add_argument(
        "--dosage1",
        "-d1",
        type=str,
        default=None,
        help="Dosage information for first medicine",
    )

    parser.add_argument(
        "--dosage2",
        "-d2",
        type=str,
        default=None,
        help="Dosage information for second medicine",
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
        type=Path,
        default=None,
        help="Output file path for results (default: outputs/{medicine1}_{medicine2}_interaction.json)",
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
        default=False,
        help="Disable schema-based prompt generation",
    )

    parser.add_argument(
        "--verbosity",
        "-v",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2).",
    )

    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="ollama/gemma3",
        help="Model ID to use for analysis (default: ollama/gemma3)",
    )

    parser.add_argument(
        "--json-output",
        "-j",
        action="store_true",
        default=False,
        help="Output results as JSON to stdout (in addition to file)",
    )

    return parser.parse_args()


# ==============================================================================
# DISPLAY/OUTPUT FUNCTIONS
# ==============================================================================


def print_result(result: DrugInteractionResult, verbose: bool = False) -> None:
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
            "SIGNIFICANT": "yellow",
            "CONTRAINDICATED": "red",
        }.get(details.severity_level.value, "white")

        # Create details panel
        details_text = (
            f"[bold]Drug 1:[/bold] {details.drug1_name}\n"
            f"[bold]Drug 2:[/bold] {details.drug2_name}\n"
            f"[bold]Severity:[/bold] [{severity_color}]{details.severity_level.value}[/{severity_color}]\n"
            f"[bold]Confidence:[/bold] {details.confidence_level.value}\n"
            f"[bold]Data Source:[/bold] {details.data_source_type.value}"
        )

        console.print(
            Panel(
                details_text,
                title="Drug Interaction Details",
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

        # Management recommendations
        recommendations = [
            rec.strip() for rec in details.management_recommendations.split(",")
        ]
        console.print("[bold cyan]Management Recommendations:[/bold cyan]")
        for rec in recommendations:
            console.print(f"  • {rec}")
        console.print()

        # Alternative medicines
        alternatives = [
            alt.strip() for alt in details.alternative_medicines.split(",")
        ]
        console.print("[bold cyan]Alternative Medicines:[/bold cyan]")
        for alt in alternatives:
            console.print(f"  • {alt}")
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

        # Warning signs
        warning_signs = [sign.strip() for sign in summary.warning_signs.split(",")]
        console.print("[bold yellow]Warning Signs:[/bold yellow]")
        for sign in warning_signs:
            console.print(f"  • {sign}")
        console.print()

        # When to seek help
        console.print(
            Panel(
                summary.when_to_seek_help,
                title="When to Seek Help",
                border_style="red",
            )
        )

    # Print technical summary
    console.print(
        Panel(
            result.technical_summary,
            title="Technical Summary",
            border_style="magenta",
        )
    )


def app_cli():
    """
    Main entry point for the drug-drug interaction CLI.

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    args = get_user_arguments()

    # Configure logging at the entry point
    configure_logging(
        log_file="drug_drug_interaction.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    try:
        # Create configuration and input
        config = DrugDrugInput(
            medicine1=args.medicine1,
            medicine2=args.medicine2,
            age=args.age if hasattr(args, 'age') else None,
            dosage1=args.dosage1 if hasattr(args, 'dosage1') else None,
            dosage2=args.dosage2 if hasattr(args, 'dosage2') else None,
            medical_conditions=args.conditions if hasattr(args, 'conditions') else None,
            output_path=args.output if hasattr(args, 'output') else None,
            prompt_style=args.prompt_style,
        )

        logger.info(f"Configuration and input created successfully")

        # Create model configuration
        model_config = ModelConfig(model=args.model, temperature=0.7)

        # Run analysis
        analyzer = DrugDrugInteraction(model_config)
        result = analyzer.analyze(config)

        # Print results
        print_result(result, verbose=args.verbosity >= 3)

        # Determine output path for saving
        output_path = config.output_path
        if output_path is None:
            medicine1_clean = args.medicine1.lower().replace(' ', '_')
            medicine2_clean = args.medicine2.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine1_clean}_{medicine2_clean}_interaction.json"

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
        return 
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        logger.error(f"Unexpected error: {e}")
        logger.exception("Full exception details:")
        return


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    app_cli()
