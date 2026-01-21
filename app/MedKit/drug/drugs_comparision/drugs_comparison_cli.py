"""Module docstring - Medicines Comparison Tool.

Compare medicines side-by-side across clinical, regulatory, and practical metrics to help
healthcare professionals and patients make informed treatment decisions.
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
from rich.table import Table

# ==============================================================================
# LOCAL IMPORTS (LiteClient setup)
# ==============================================================================
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging

# ==============================================================================
# LOCAL IMPORTS (Module models)
# ==============================================================================
from drugs_comparison_models import (
    MedicinesComparisonResult,
)

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================
logger = logging.getLogger(__name__)


# ==============================================================================
# CONSTANTS
# ==============================================================================
console = Console()


# ==============================================================================
# CONFIGURATION CLASS
# ==============================================================================

@dataclass
class DrugsComparisonConfig:
    """Configuration for drugs comparison."""
    output_path: Optional[Path] = None
    verbosity: int = 2  # 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG
    enable_cache: bool = True

# ==============================================================================
# MAIN CLASS
# ==============================================================================

class DrugsComparison:
    """Compares two medicines based on provided configuration."""

    def __init__(self, config: DrugsComparisonConfig, model_config: ModelConfig):
        self.config = config
        self.client = LiteClient(model_config)

        # Apply verbosity level using centralized logging configuration
        configure_logging(
            log_file="drugs_comparison.log",
            verbosity=self.config.verbosity,
            enable_console=True
        )

    def compare(
        self,
        medicine1: str,
        medicine2: str,
        use_case: Optional[str] = None,
        patient_age: Optional[int] = None,
        patient_conditions: Optional[str] = None,
    ) -> MedicinesComparisonResult:
        """
        Compares two medicines across clinical, regulatory, and practical metrics.

        Args:
            medicine1: Name of the first medicine
            medicine2: Name of the second medicine
            use_case: Use case or indication for comparison (optional)
            patient_age: Patient's age in years (optional, 0-150)
            patient_conditions: Patient's medical conditions (optional, comma-separated)

        Returns:
            MedicinesComparisonResult: Comprehensive side-by-side comparison
        """
        # Validate inputs
        if not medicine1 or not medicine1.strip():
            raise ValueError("Medicine 1 name cannot be empty")
        if not medicine2 or not medicine2.strip():
            raise ValueError("Medicine 2 name cannot be empty")
        if patient_age is not None and (patient_age < 0 or patient_age > 150):
            raise ValueError("Age must be between 0 and 150 years")

        logger.info("-" * 80)
        logger.info(f"Starting drugs comparison analysis")
        logger.info(f"Medicine 1: {medicine1}")
        logger.info(f"Medicine 2: {medicine2}")

        output_path = self.config.output_path
        if output_path is None:
            medicine1_clean = medicine1.lower().replace(' ', '_')
            medicine2_clean = medicine2.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine1_clean}_vs_{medicine2_clean}_comparison.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path}")

        context_parts = [f"Comparing {medicine1} and {medicine2}"]
        if use_case:
            context_parts.append(f"Use case: {use_case}")
            logger.info(f"Use case: {use_case}")
        if patient_age is not None:
            context_parts.append(f"Patient age: {patient_age} years")
            logger.info(f"Patient age: {patient_age}")
        if patient_conditions:
            context_parts.append(f"Patient conditions: {patient_conditions}")
            logger.info(f"Patient conditions: {patient_conditions}")

        context = ". ".join(context_parts) + "."
        logger.debug(f"Context: {context}")

        logger.info("Calling LiteClient.generate_text()...")
        try:
            result = self.client.generate_text(
                model_input=ModelInput(
                    user_prompt=f"Detailed side-by-side comparison between {medicine1} and {medicine2}. {context}",
                    response_format=MedicinesComparisonResult,
                )
            )

            logger.info(f"✓ Successfully compared medicines")
            logger.info(f"More Effective: {result.comparison_summary.more_effective[:100] if result.comparison_summary.more_effective else 'N/A'}...")
            logger.info(f"More Affordable: {result.comparison_summary.more_affordable[:100] if result.comparison_summary.more_affordable else 'N/A'}...")
            logger.info("-" * 80)
            return result
        except Exception as e:
            logger.error(f"✗ Error comparing medicines: {e}")
            logger.exception("Full exception details:")
            logger.info("-" * 80)
            raise


def get_drugs_comparison(
    medicine1: str,
    medicine2: str,
    config: DrugsComparisonConfig,
    model_config: ModelConfig,
    use_case: Optional[str] = None,
    patient_age: Optional[int] = None,
    patient_conditions: Optional[str] = None,
) -> MedicinesComparisonResult:
    """
    Get drugs comparison.

    This is a convenience function that instantiates and runs the
    DrugsComparison analyzer.

    Args:
        medicine1: Name of the first medicine
        medicine2: Name of the second medicine
        config: Configuration object for the analysis
        model_config: ModelConfig object containing model settings
        use_case: Use case or indication for comparison (optional)
        patient_age: Patient's age in years (optional)
        patient_conditions: Patient's medical conditions (optional)

    Returns:
        MedicinesComparisonResult: The result of the analysis
    """
    analyzer = DrugsComparison(config, model_config)
    return analyzer.compare(
        medicine1=medicine1,
        medicine2=medicine2,
        use_case=use_case,
        patient_age=patient_age,
        patient_conditions=patient_conditions,
    )


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================


def create_cli_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser for the CLI.

    Returns:
        argparse.ArgumentParser: Configured parser for command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Medicines Comparison Tool - Compare two medicines side-by-side",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic comparison
  python drugs_comparison.py "Aspirin" "Ibuprofen"

  # With use case
  python drugs_comparison.py "Lisinopril" "Losartan" --use-case "hypertension management"

  # With patient details
  python drugs_comparison.py "Metformin" "Glipizide" --age 68 --conditions "type-2 diabetes, kidney disease"

  # With custom output
  python drugs_comparison.py "Atorvastatin" "Simvastatin" --output comparison.json --verbose
        """,
    )

    # Required arguments
    parser.add_argument(
        "medicine1",
        type=str,
        help="Name of the first medicine to compare",
    )

    parser.add_argument(
        "medicine2",
        type=str,
        help="Name of the second medicine to compare",
    )

    # Optional arguments
    parser.add_argument(
        "--use-case",
        "-u",
        type=str,
        default=None,
        help="Use case or indication for the comparison (e.g., 'pain relief', 'hypertension')",
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
        type=Path,
        default=None,
        help="Output file path for results (default: outputs/{medicine1}_vs_{medicine2}_comparison.json)",
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

    return parser


# ==============================================================================
# DISPLAY/OUTPUT FUNCTIONS
# ==============================================================================


def print_result(result: MedicinesComparisonResult, verbose: bool = False) -> None:
    """
    Print comparison results in a formatted manner using rich.

    Args:
        result: The analysis result to print
        verbose: Whether to print detailed information
    """
    console = Console()

    # Print comparison summary
    summary = result.comparison_summary
    summary_text = (
        f"[bold]More Effective:[/bold] {summary.more_effective}\n"
        f"[bold]Safer Option:[/bold] {summary.safer_option}\n"
        f"[bold]More Affordable:[/bold] {summary.more_affordable}\n"
        f"[bold]Easier Access:[/bold] {summary.easier_access}\n\n"
        f"[bold]Key Differences:[/bold]"
    )

    console.print(
        Panel(
            summary_text,
            title="Comparison Summary",
            border_style="cyan",
        )
    )

    differences = [diff.strip() for diff in summary.key_differences.split(",")]
    for diff in differences:
        console.print(f"  • {diff}")
    console.print()

    # Clinical metrics table
    clinical_table = Table(title="Clinical Metrics", border_style="blue")
    clinical_table.add_column("Metric", style="cyan")
    clinical_table.add_column(result.medicine1_clinical.medicine_name, style="magenta")
    clinical_table.add_column(result.medicine2_clinical.medicine_name, style="magenta")

    clinical_table.add_row(
        "Effectiveness",
        result.medicine1_clinical.effectiveness_rating.value,
        result.medicine2_clinical.effectiveness_rating.value,
    )
    clinical_table.add_row(
        "Efficacy Rate",
        result.medicine1_clinical.efficacy_rate,
        result.medicine2_clinical.efficacy_rate,
    )
    clinical_table.add_row(
        "Onset of Action",
        result.medicine1_clinical.onset_of_action,
        result.medicine2_clinical.onset_of_action,
    )
    clinical_table.add_row(
        "Safety Rating",
        result.medicine1_clinical.safety_rating.value,
        result.medicine2_clinical.safety_rating.value,
    )

    console.print(clinical_table)

    # Black box warnings if present
    if result.medicine1_clinical.black_box_warning or result.medicine2_clinical.black_box_warning:
        console.print("[bold yellow]Black Box Warnings:[/bold yellow]")
        if result.medicine1_clinical.black_box_warning:
            console.print(f"  {result.medicine1_clinical.medicine_name}: {result.medicine1_clinical.black_box_warning}")
        if result.medicine2_clinical.black_box_warning:
            console.print(f"  {result.medicine2_clinical.medicine_name}: {result.medicine2_clinical.black_box_warning}")
        console.print()

    # Regulatory information table
    reg_table = Table(title="Regulatory Information", border_style="blue")
    reg_table.add_column("Aspect", style="cyan")
    reg_table.add_column(result.medicine1_regulatory.medicine_name, style="magenta")
    reg_table.add_column(result.medicine2_regulatory.medicine_name, style="magenta")

    reg_table.add_row(
        "FDA Status",
        result.medicine1_regulatory.fda_approval_status,
        result.medicine2_regulatory.fda_approval_status,
    )
    reg_table.add_row(
        "Approval Date",
        result.medicine1_regulatory.approval_date,
        result.medicine2_regulatory.approval_date,
    )
    reg_table.add_row(
        "Approval Type",
        result.medicine1_regulatory.approval_type,
        result.medicine2_regulatory.approval_type,
    )
    reg_table.add_row(
        "Generic Available",
        "Yes" if result.medicine1_regulatory.generic_available else "No",
        "Yes" if result.medicine2_regulatory.generic_available else "No",
    )

    console.print(reg_table)

    # Practical information table
    practical_table = Table(title="Practical Information", border_style="blue")
    practical_table.add_column("Aspect", style="cyan")
    practical_table.add_column(result.medicine1_practical.medicine_name, style="magenta")
    practical_table.add_column(result.medicine2_practical.medicine_name, style="magenta")

    practical_table.add_row(
        "Availability",
        result.medicine1_practical.availability_status.value,
        result.medicine2_practical.availability_status.value,
    )
    practical_table.add_row(
        "Typical Cost",
        result.medicine1_practical.typical_cost_range,
        result.medicine2_practical.typical_cost_range,
    )
    practical_table.add_row(
        "Insurance Coverage",
        result.medicine1_practical.insurance_coverage,
        result.medicine2_practical.insurance_coverage,
    )

    console.print(practical_table)

    # Print recommendations
    recs = result.recommendations
    console.print("[bold cyan]Clinical Recommendations:[/bold cyan]")

    if recs.for_acute_conditions:
        console.print(
            Panel(
                recs.for_acute_conditions,
                title="For Acute Conditions",
                border_style="green",
            )
        )

    if recs.for_chronic_conditions:
        console.print(
            Panel(
                recs.for_chronic_conditions,
                title="For Chronic Conditions",
                border_style="green",
            )
        )

    if recs.for_elderly_patients:
        console.print(
            Panel(
                recs.for_elderly_patients,
                title="For Elderly Patients",
                border_style="green",
            )
        )

    if recs.for_cost_sensitive:
        console.print(
            Panel(
                recs.for_cost_sensitive,
                title="For Cost-Sensitive Patients",
                border_style="green",
            )
        )

    console.print(
        Panel(
            recs.overall_recommendation,
            title="Overall Recommendation",
            border_style="cyan",
        )
    )

    # Print narrative analysis
    console.print(
        Panel(
            result.narrative_analysis,
            title="Detailed Analysis",
            border_style="magenta",
        )
    )

    # Print evidence quality and limitations
    console.print(
        Panel(
            result.evidence_quality,
            title="Evidence Quality",
            border_style="yellow",
        )
    )

    console.print("[bold yellow]Limitations:[/bold yellow]")
    limitations = [lim.strip() for lim in result.limitations.split(",")]
    for lim in limitations:
        console.print(f"  • {lim}")


# ==============================================================================
# ARGUMENT PARSER
# ==============================================================================


# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main() -> int:
    """
    Main entry point for the drugs comparison CLI.

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    parser = create_cli_parser()
    args = parser.parse_args()

    try:
        # Create configuration
        config = DrugsComparisonConfig(
            output_path=args.output if hasattr(args, 'output') else None,
            verbosity=args.verbosity,
        )

        logger.info(f"Configuration created successfully")

        # Run analysis
        model_config = ModelConfig(model="ollama/gemma2", temperature=0.7)
        analyzer = DrugsComparison(config, model_config)
        result = analyzer.compare(
            medicine1=args.medicine1,
            medicine2=args.medicine2,
            use_case=args.use_case if hasattr(args, 'use_case') else None,
            patient_age=args.age if hasattr(args, 'age') else None,
            patient_conditions=args.conditions if hasattr(args, 'conditions') else None,
        )

        # Print results
        print_result(result, verbose=args.verbosity >= 3)

        # Save results to file
        if args.output:
            output_path = args.output
        else:
            medicine1_clean = args.medicine1.lower().replace(' ', '_')
            medicine2_clean = args.medicine2.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine1_clean}_vs_{medicine2_clean}_comparison.json"

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
