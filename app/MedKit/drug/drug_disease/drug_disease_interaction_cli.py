"""Drug-Disease Interaction Analysis module."""

import argparse
import logging
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging

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

logger = logging.getLogger(__name__)
console = Console()


class PromptStyle(str, Enum):
    DETAILED = "detailed"
    CONCISE = "concise"
    BALANCED = "balanced"

@dataclass
class DrugDiseaseInput:
    """Configuration and input for drug-disease interaction analysis."""
    medicine_name: str
    condition_name: str
    condition_severity: Optional[str] = None
    age: Optional[int] = None
    other_medications: Optional[str] = None
    output_path: Optional[Path] = None
    prompt_style: PromptStyle = PromptStyle.DETAILED

# ==============================================================================
# MAIN CLASS
# ==============================================================================

class DrugDiseaseInteraction:
    """Analyzes drug-disease interactions based on provided configuration."""
    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def _validate_input(self, config: DrugDiseaseInput) -> None:
        """Validate input parameters."""
        if not config.medicine_name or not config.medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")
        if not config.condition_name or not config.condition_name.strip():
            raise ValueError("Condition name cannot be empty")
        if config.age is not None and (config.age < 0 or config.age > 150):
            raise ValueError("Age must be between 0 and 150 years")

    def _get_output_path(self, config: DrugDiseaseInput) -> Path:
        """Determine the file path for saving analysis results."""
        if config.output_path:
            return config.output_path
        
        medicine_clean = config.medicine_name.lower().replace(' ', '_')
        condition_clean = config.condition_name.lower().replace(' ', '_')
        return Path("outputs") / f"{medicine_clean}_{condition_clean}_interaction.json"

    def _prepare_context(self, config: DrugDiseaseInput) -> str:
        """Build the analysis context string from input parameters."""
        context_parts = [f"Analyzing interaction between {config.medicine_name} and {config.condition_name}"]
        
        if config.condition_severity:
            context_parts.append(f"Condition severity: {config.condition_severity}")
            logger.info(f"Condition severity: {config.condition_severity}")
        if config.age is not None:
            context_parts.append(f"Patient age: {config.age} years")
            logger.info(f"Patient age: {config.age}")
        if config.other_medications:
            context_parts.append(f"Other medications: {config.other_medications}")
            logger.info(f"Other medications: {config.other_medications}")

        return ". ".join(context_parts) + "."

    def _execute_llm_analysis(self, config: DrugDiseaseInput, context: str) -> DrugDiseaseInteractionResult:
        """Call LiteClient to perform the interaction analysis."""
        logger.info("Calling LiteClient...")
        try:
            return self.client.generate_text(
                model_input=ModelInput(
                    user_prompt=f"{config.medicine_name} use in patients with {config.condition_name}. {context}",
                    response_format=DrugDiseaseInteractionResult,
                )
            )
        except Exception as e:
            logger.error(f"✗ Error analyzing disease interaction: {e}")
            logger.exception("Full exception details:")
            raise

    def analyze(self, config: DrugDiseaseInput) -> DrugDiseaseInteractionResult:
        """
        Analyzes how a medical condition affects drug efficacy, safety, and metabolism.

        Args:
            config: Configuration and input for analysis

        Returns:
            DrugDiseaseInteractionResult: Comprehensive interaction analysis with management recommendations
        """
        self._validate_input(config)

        logger.info("-" * 80)
        logger.info(f"Starting drug-disease interaction analysis")
        logger.info(f"Medicine: {config.medicine_name}")
        logger.info(f"Condition: {config.condition_name}")

        output_path = self._get_output_path(config)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path}")

        context = self._prepare_context(config)
        logger.debug(f"Context: {context}")

        result = self._execute_llm_analysis(config, context)

        logger.info(f"✓ Successfully analyzed disease interaction")
        logger.info(f"Overall Severity: {result.interaction_details.overall_severity if result.interaction_details else 'N/A'}")
        logger.info(f"Data Available: {result.data_availability.data_available}")
        logger.info("-" * 80)
        return result

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

def get_user_arguments():
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
        "--verbosity",
        "-v",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2).",
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

    return parser.parse_args()

def main() -> int:
    """
    Main entry point for the drug-disease interaction CLI.

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    args  = get_user_arguments()

    try:
        # Parse prompt style
        prompt_style = parse_prompt_style(args.prompt_style)

        # Configure logging
        configure_logging(
            log_file="drug_disease_interaction.log",
            verbosity=args.verbosity,
            enable_console=True
        )

        # Create configuration
        config = DrugDiseaseInput(
            medicine_name=args.medicine_name,
            condition_name=args.condition_name,
            condition_severity=args.condition_severity,
            age=args.age,
            other_medications=args.other_medications,
            output_path=args.output,
            prompt_style=prompt_style,
        )

        logger.info(f"Configuration created successfully")

        # Run analysis
        model_config = ModelConfig(model=args.model, temperature=0.7)
        analyzer = DrugDiseaseInteraction(model_config)
        result = analyzer.analyze(config)

        # Print results
        print_result(result, verbose=args.verbosity >= 3)

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
