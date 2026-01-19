"""Drug-Disease Interaction Analysis module."""

# ==============================================================================
# STANDARD LIBRARY IMPORTS
# ==============================================================================
import argparse
import json
import logging
import sys
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ==============================================================================
# THIRD-PARTY IMPORTS
# ==============================================================================
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
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
from drug_disease_interaction_models import (
    InteractionSeverity,
    ConfidenceLevel,
    DataSourceType,
    ImpactType,
    EfficacyImpact,
    SafetyImpact,
    DosageAdjustment,
    ManagementStrategy,
    DrugDiseaseInteractionDetails,
    PatientFriendlySummary,
    DataAvailabilityInfo,
    DrugDiseaseInteractionResult,
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
# ENUMS
# ==============================================================================
class PromptStyle(str, Enum):
    DETAILED = "detailed"
    CONCISE = "concise"
    BALANCED = "balanced"

# ==============================================================================
# CONFIGURATION CLASS
# ==============================================================================
@dataclass
class DrugDiseaseInteractionConfig:
    """Configuration for drug-disease interaction analysis."""
    output_path: Optional[Path] = None
    verbosity: bool = False
    prompt_style: PromptStyle = PromptStyle.DETAILED
    enable_cache: bool = True
    model: str = "ollama/gemma3"

# ==============================================================================
# MAIN CLASS
# ==============================================================================
class DrugDiseaseInteraction:
    """Analyzes drug-disease interactions based on provided configuration."""

    def __init__(self, config: DrugDiseaseInteractionConfig):
        self.config = config
        self.client = LiteClient(
            ModelConfig(model=config.model, temperature=0.7)
        )

    def analyze(
        self,
        medicine_name: str,
        condition_name: str,
        condition_severity: Optional[str] = None,
        age: Optional[int] = None,
        other_medications: Optional[str] = None,
    ) -> DrugDiseaseInteractionResult:
        """
        Analyzes how a medical condition affects drug efficacy, safety, and metabolism.

        Args:
            medicine_name: Name of the medicine to analyze
            condition_name: Name of the medical condition
            condition_severity: Severity of the condition (optional)
            age: Patient age in years (optional, 0-150)
            other_medications: Other medications patient is taking (optional, comma-separated)

        Returns:
            DrugDiseaseInteractionResult: Comprehensive interaction analysis with management recommendations
        """
        # Validate inputs
        if not medicine_name or not medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")
        if not condition_name or not condition_name.strip():
            raise ValueError("Condition name cannot be empty")
        if age is not None and (age < 0 or age > 150):
            raise ValueError("Age must be between 0 and 150 years")

        logger.info("-" * 80)
        logger.info(f"Starting drug-disease interaction analysis")
        logger.info(f"Medicine: {medicine_name}")
        logger.info(f"Condition: {condition_name}")

        output_path = self.config.output_path
        if output_path is None:
            medicine_clean = medicine_name.lower().replace(' ', '_')
            condition_clean = condition_name.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine_clean}_{condition_clean}_interaction.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path}")

        context_parts = [f"Analyzing interaction between {medicine_name} and {condition_name}"]
        if condition_severity:
            context_parts.append(f"Condition severity: {condition_severity}")
            logger.info(f"Condition severity: {condition_severity}")
        if age is not None:
            context_parts.append(f"Patient age: {age} years")
            logger.info(f"Patient age: {age}")
        if other_medications:
            context_parts.append(f"Other medications: {other_medications}")
            logger.info(f"Other medications: {other_medications}")

        context = ". ".join(context_parts) + "."
        logger.debug(f"Context: {context}")

        logger.info("Calling LiteClient...")
        try:
            result = self.client.generate_text(
                model_input=ModelInput(
                    user_prompt=f"{medicine_name} use in patients with {condition_name}. {context}",
                    response_format=DrugDiseaseInteractionResult,
                )
            )

            logger.info(f"✓ Successfully analyzed disease interaction")
            logger.info(f"Overall Severity: {result.interaction_details.overall_severity if result.interaction_details else 'N/A'}")
            logger.info(f"Data Available: {result.data_availability.data_available}")
            logger.info("-" * 80)
            return result
        except Exception as e:
            logger.error(f"✗ Error analyzing disease interaction: {e}")
            logger.exception("Full exception details:")
            logger.info("-" * 80)
            raise

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def parse_prompt_style(style_str: str) -> PromptStyle:
    """
    Parse prompt style string to PromptStyle enum.

    Args:
        style_str: String representation of prompt style

    Returns:
        PromptStyle: The corresponding enum value

    Raises:
        ValueError: If style string is not a valid prompt style
    """
    style_mapping = {
        "detailed": PromptStyle.DETAILED,
        "concise": PromptStyle.CONCISE,
        "balanced": PromptStyle.BALANCED,
    }

    if style_str.lower() not in style_mapping:
        raise ValueError(
            f"Invalid prompt style: {style_str}. "
            f"Choose from: {', '.join(style_mapping.keys())}"
        )

    return style_mapping[style_str.lower()]

# ==============================================================================
# DISPLAY/OUTPUT FUNCTIONS
# ==============================================================================
def print_result(result: DrugDiseaseInteractionResult, verbose: bool = False) -> None:
    """
    Print interaction analysis results in a formatted manner using rich formatting.

    Args:
        result: The analysis result to print
        verbose: Whether to print detailed information
    """
    console.print()

    # Check data availability
    if not result.data_availability.data_available:
        console.print(
            Panel(
                f"⚠️  [yellow]{result.data_availability.reason}[/yellow]",
                title="[bold red]Data Unavailable[/bold red]",
                border_style="red"
            )
        )
        return

    # Main title
    console.print(
        Panel.fit(
            "[bold cyan]DRUG-DISEASE INTERACTION ANALYSIS[/bold cyan]",
            border_style="cyan"
        )
    )

    # Print interaction details
    if result.interaction_details:
        details = result.interaction_details

        # Overview table
        overview_table = Table(title="[bold]Interaction Overview[/bold]", show_header=False, box=None)
        overview_table.add_row("[bold]Medicine:[/bold]", details.medicine_name)
        overview_table.add_row("[bold]Condition:[/bold]", details.condition_name)

        severity_color = "red" if "CONTRAINDICATED" in details.overall_severity.value else "yellow" if "SEVERE" in details.overall_severity.value else "green"
        overview_table.add_row("[bold]Severity:[/bold]", f"[{severity_color}]{details.overall_severity.value}[/{severity_color}]")
        overview_table.add_row("[bold]Confidence:[/bold]", details.confidence_level.value)
        overview_table.add_row("[bold]Data Source:[/bold]", details.data_source_type.value)

        console.print(overview_table)
        console.print()

        # Mechanism of interaction
        console.print(
            Panel(
                details.mechanism_of_interaction,
                title="[bold]Mechanism of Interaction[/bold]",
                border_style="blue"
            )
        )

        # Efficacy impact
        efficacy_content = "No significant impact on drug efficacy"
        if details.efficacy_impact.has_impact:
            efficacy_lines = []
            if details.efficacy_impact.impact_description:
                efficacy_lines.append(f"[bold]Impact:[/bold] {details.efficacy_impact.impact_description}")
            if details.efficacy_impact.clinical_significance:
                efficacy_lines.append(f"[bold]Significance:[/bold] {details.efficacy_impact.clinical_significance}")
            efficacy_content = "\n".join(efficacy_lines) if efficacy_lines else "Impact detected"

        console.print(
            Panel(
                efficacy_content,
                title="[bold yellow]Efficacy Impact[/bold yellow]",
                border_style="yellow"
            )
        )

        # Safety impact
        safety_content = "No significant safety concerns"
        if details.safety_impact.has_impact:
            safety_lines = []
            if details.safety_impact.impact_description:
                safety_lines.append(f"[bold]Risk:[/bold] {details.safety_impact.impact_description}")
            if details.safety_impact.risk_level:
                risk_color = "red" if "HIGH" in details.safety_impact.risk_level.value else "yellow"
                safety_lines.append(f"[bold]Risk Level:[/bold] [{risk_color}]{details.safety_impact.risk_level.value}[/{risk_color}]")
            safety_content = "\n".join(safety_lines) if safety_lines else "Safety concerns identified"

        console.print(
            Panel(
                safety_content,
                title="[bold red]Safety Impact[/bold red]",
                border_style="red"
            )
        )

        # Dosage adjustments
        dosage_content = "No dose adjustment required"
        if details.dosage_adjustment.adjustment_needed:
            dosage_lines = []
            if details.dosage_adjustment.adjustment_type:
                dosage_lines.append(f"[bold]Type:[/bold] {details.dosage_adjustment.adjustment_type}")
            if details.dosage_adjustment.specific_recommendations:
                dosage_lines.append(f"[bold]Details:[/bold] {details.dosage_adjustment.specific_recommendations}")
            dosage_content = "\n".join(dosage_lines) if dosage_lines else "Adjustment recommended"

        console.print(
            Panel(
                dosage_content,
                title="[bold magenta]Dosage Adjustments[/bold magenta]",
                border_style="magenta"
            )
        )

        # Management recommendations
        recommendations = [rec.strip() for rec in details.management_strategy.clinical_recommendations.split(",")]
        recommendations_text = "\n".join([f"• {rec}" for rec in recommendations])
        console.print(
            Panel(
                recommendations_text,
                title="[bold green]Management Recommendations[/bold green]",
                border_style="green"
            )
        )

    # Patient-friendly summary
    if result.patient_friendly_summary:
        summary = result.patient_friendly_summary
        console.print()
        console.print(
            Panel.fit(
                "[bold cyan]PATIENT-FRIENDLY GUIDANCE[/bold cyan]",
                border_style="cyan"
            )
        )

        console.print(
            Panel(
                summary.simple_explanation,
                title="[bold]Simple Explanation[/bold]",
                border_style="blue"
            )
        )

        console.print(
            Panel(
                summary.what_patient_should_do,
                title="[bold]What You Should Do[/bold]",
                border_style="green"
            )
        )

        signs = [sign.strip() for sign in summary.signs_of_problems.split(",")]
        signs_text = "\n".join([f"• {sign}" for sign in signs])
        console.print(
            Panel(
                signs_text,
                title="[bold red]Signs of Problems[/bold red]",
                border_style="red"
            )
        )

        console.print(
            Panel(
                summary.when_to_contact_doctor,
                title="[bold]When to Contact Doctor[/bold]",
                border_style="yellow"
            )
        )

    # Technical summary
    console.print()
    console.print(
        Panel(
            result.technical_summary,
            title="[bold]Technical Summary[/bold]",
            border_style="dim"
        )
    )
    console.print()

# ==============================================================================
# ARGUMENT PARSER
# ==============================================================================
def create_argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser for the CLI.

    Returns:
        argparse.ArgumentParser: Configured parser for command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Drug-Disease Interaction Analyzer - Assess how medical conditions affect medicines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  python drug_disease_interaction.py "Metformin" "Kidney Disease"

  # With condition severity
  python drug_disease_interaction.py "Warfarin" "Liver Disease" --condition-severity severe

  # With patient details and other medications
  python drug_disease_interaction.py "Lisinopril" "Hypertension" --age 72 --other-medications "Atorvastatin, Aspirin"

  # With custom output
  python drug_disease_interaction.py "NSAIDs" "Asthma" --output interaction.json --verbose
        """,
    )

    # Required arguments
    parser.add_argument(
        "medicine_name",
        type=str,
        help="Name of the medicine to analyze",
    )

    parser.add_argument(
        "condition_name",
        type=str,
        help="Name of the medical condition",
    )

    # Optional arguments
    parser.add_argument(
        "--condition-severity",
        "-s",
        type=str,
        default=None,
        help="Severity of the condition (mild, moderate, severe)",
    )

    parser.add_argument(
        "--age",
        "-a",
        type=int,
        default=None,
        help="Patient's age in years (0-150)",
    )

    parser.add_argument(
        "--other-medications",
        "-m",
        type=str,
        default=None,
        help="Other medications the patient is taking (comma-separated)",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output file path for results (default: outputs/{medicine}_{condition}_interaction.json)",
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
        "--verbose",
        "-v",
        action="store_true",
        default=False,
        help="Enable verbose logging output",
    )

    parser.add_argument(
        "--json-output",
        "-j",
        action="store_true",
        default=False,
        help="Output results as JSON to stdout (in addition to file)",
    )

    parser.add_argument(
        "--model",
        type=str,
        default="ollama/gemma3",
        help="LLM model to use for analysis (default: ollama/gemma3)",
    )

    return parser

# ==============================================================================
# MAIN FUNCTION
# ==============================================================================
def main() -> int:
    """
    Main entry point for the drug-disease interaction CLI.

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    parser = create_argument_parser()
    args = parser.parse_args()

    # Configure logging verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    try:
        # Parse prompt style
        prompt_style = parse_prompt_style(args.prompt_style)

        # Create configuration
        config = DrugDiseaseInteractionConfig(
            output_path=args.output,
            verbosity=args.verbose,
            prompt_style=prompt_style,
            model=args.model,
        )

        logger.info(f"Configuration created successfully")

        # Run analysis
        analyzer = DrugDiseaseInteraction(config)
        result = analyzer.analyze(
            medicine_name=args.medicine_name,
            condition_name=args.condition_name,
            condition_severity=args.condition_severity,
            age=args.age,
            other_medications=args.other_medications,
        )

        # Print results
        print_result(result, verbose=args.verbose)

        # Save results to file
        if args.output:
            output_path = args.output
        else:
            medicine_clean = args.medicine_name.lower().replace(' ', '_')
            condition_clean = args.condition_name.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine_clean}_{condition_clean}_interaction.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            f.write(result.model_dump_json(indent=2))

        logger.info(f"✓ Results saved to {output_path}")
        console.print(f"[green]✓[/green] Results saved to: [bold]{output_path}[/bold]")

        # Output JSON to stdout if requested
        if args.json_output:
            console.print(f"\n{result.model_dump_json(indent=2)}")

        return 0

    except ValueError as e:
        console.print(f"[red]✗[/red] Invalid input: {e}", style="bold red")
        logger.error(f"Invalid input: {e}")
        return 1
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}", style="bold red")
        logger.error(f"Unexpected error: {e}")
        logger.exception("Full exception details:")
        return 1

# ==============================================================================
# ENTRY POINT
# ==============================================================================


if __name__ == "__main__":
    sys.exit(main())
