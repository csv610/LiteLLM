"""Module docstring - Similar Medicines Finder and Comparator.

Find alternative medicines with similar active ingredients, therapeutic classes, and
mechanisms of action. Provides detailed comparisons to help identify suitable substitutes.
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
from similar_drugs_models import (
    SimilarityCategory,
    EfficacyComparison,
    SimilarMedicineDetail,
    SimilarMedicinesCategory,
    SwitchingGuidance,
    SimilarMedicinesResult,
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
class SimilarDrugsConfig:
    """Configuration for finding similar drugs."""
    output_path: Optional[Path] = None
    verbosity: int = 2  # 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG
    enable_cache: bool = True

# ==============================================================================
# MAIN CLASS
# ==============================================================================

class SimilarDrugs:
    """Finds similar drugs based on provided configuration."""

    def __init__(self, config: SimilarDrugsConfig, model_config: ModelConfig):
        self.config = config
        self.client = LiteClient(model_config)

        # Apply verbosity level using centralized logging configuration
        configure_logging(
            log_file="similar_drugs.log",
            verbosity=self.config.verbosity,
            enable_console=True
        )

    def find(
        self,
        medicine_name: str,
        include_generics: bool = True,
        patient_age: Optional[int] = None,
        patient_conditions: Optional[str] = None,
    ) -> SimilarMedicinesResult:
        """
        Finds top 10-15 medicines similar to a given medicine.

        Args:
            medicine_name: Name of the medicine to find alternatives for
            include_generics: Whether to include generic formulations (default: True)
            patient_age: Patient's age in years (optional, 0-150)
            patient_conditions: Patient's medical conditions (optional, comma-separated)

        Returns:
            SimilarMedicinesResult: Top 10-15 similar medicines with detailed information
        """
        # Validate inputs
        if not medicine_name or not medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")
        if patient_age is not None and (patient_age < 0 or patient_age > 150):
            raise ValueError("Age must be between 0 and 150 years")

        output_path = self.config.output_path
        if output_path is None:
            medicine_clean = medicine_name.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine_clean}_similar_medicines.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        context_parts = [f"Finding top 10-15 medicines similar to {medicine_name}"]
        if include_generics:
            context_parts.append("Include generic formulations")
        if patient_age is not None:
            context_parts.append(f"Patient age: {patient_age} years")
        if patient_conditions:
            context_parts.append(f"Patient conditions: {patient_conditions}")

        context = ". ".join(context_parts) + "."

        result = self.client.generate_text(
            model_input=ModelInput(
                user_prompt=f"Find the top 10-15 most similar medicines to {medicine_name} - prioritize same active ingredients, then therapeutic class, then similar mechanism. {context}",
                response_format=SimilarMedicinesResult,
            )
        )

        return result


def get_similar_medicines(
    medicine_name: str,
    config: SimilarDrugsConfig,
    model_config: ModelConfig,
    include_generics: bool = True,
    patient_age: Optional[int] = None,
    patient_conditions: Optional[str] = None,
) -> SimilarMedicinesResult:
    """
    Get similar medicines.

    This is a convenience function that instantiates and runs the
    SimilarDrugs finder.

    Args:
        medicine_name: Name of the medicine to find alternatives for
        config: Configuration object for the analysis
        model_config: ModelConfig object containing model settings
        include_generics: Whether to include generic formulations (default: True)
        patient_age: Patient's age in years (optional)
        patient_conditions: Patient's medical conditions (optional)

    Returns:
        SimilarMedicinesResult: The result of the analysis
    """
    finder = SimilarDrugs(config, model_config)
    return finder.find(
        medicine_name=medicine_name,
        include_generics=include_generics,
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
        description="Similar Drugs Finder - Find alternative medicines and similar drug options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  python similar_drugs.py "Ibuprofen"

  # Include generics
  python similar_drugs.py "Aspirin" --include-generics

  # With patient details
  python similar_drugs.py "Metformin" --age 65 --conditions "kidney disease, hypertension"

  # With custom output
  python similar_drugs.py "Simvastatin" --output alternatives.json --verbose
        """,
    )

    # Required arguments
    parser.add_argument(
        "medicine_name",
        type=str,
        help="Name of the medicine to find similar alternatives for",
    )

    # Optional arguments
    parser.add_argument(
        "--include-generics",
        action="store_true",
        default=True,
        help="Include generic formulations (default: True)",
    )

    parser.add_argument(
        "--no-generics",
        dest="include_generics",
        action="store_false",
        help="Exclude generic formulations",
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
        help="Output file path for results (default: outputs/{medicine}_similar_medicines.json)",
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


def print_result(result: SimilarMedicinesResult, verbose: bool = False) -> None:
    """
    Print similar medicines results in a formatted manner using rich.

    Args:
        result: The analysis result to print
        verbose: Whether to print detailed information
    """
    console = Console()

    # Print original medicine info
    original_info = (
        f"[bold]Original Medicine:[/bold] {result.original_medicine}\n"
        f"[bold]Active Ingredients:[/bold] {result.original_active_ingredients}\n"
        f"[bold]Therapeutic Use:[/bold] {result.original_therapeutic_use}\n"
        f"[bold]Similar Medicines Found:[/bold] {result.total_similar_medicines_found}"
    )
    console.print(
        Panel(
            original_info,
            title="Original Medicine Information",
            border_style="cyan",
        )
    )

    # Print top recommended
    console.print(
        Panel(
            result.top_recommended,
            title="Top Recommended Alternatives",
            border_style="green",
        )
    )

    # Print categorized results
    console.print("[bold cyan]Similar Medicines by Category:[/bold cyan]")
    for category in result.categorized_results:
        category_text = (
            f"[bold]{category.category.value}[/bold]\n"
            f"Count: {category.count}\n"
            f"Summary: {category.category_summary}"
        )
        console.print(
            Panel(
                category_text,
                border_style="blue",
            )
        )

        if verbose:
            console.print("[dim]Detailed Medicines:[/dim]")
            for medicine in category.medicines:
                med_details = (
                    f"[bold]#{medicine.rank} - {medicine.medicine_name}[/bold]\n"
                    f"  Similarity Score: {medicine.similarity_score}%\n"
                    f"  Efficacy: {medicine.efficacy_comparison.value}\n"
                )
                if medicine.brand_names:
                    med_details += f"  Brand Names: {medicine.brand_names}\n"
                med_details += f"  Cost Range: {medicine.typical_cost_range}"
                if medicine.generic_available:
                    med_details += "\n  Generic Available: Yes"
                console.print(med_details)

    # Print switching guidance
    guidance = result.switching_guidance

    console.print(
        Panel(
            guidance.transition_recommendations,
            title="Transition Recommendations",
            border_style="yellow",
        )
    )

    # Switching considerations
    console.print("[bold yellow]Switching Considerations:[/bold yellow]")
    considerations = [c.strip() for c in guidance.switching_considerations.split(",")]
    for consideration in considerations:
        console.print(f"  • {consideration}")
    console.print()

    # Monitoring during switch
    console.print("[bold yellow]Monitoring During Switch:[/bold yellow]")
    monitoring = [m.strip() for m in guidance.monitoring_during_switch.split(",")]
    for item in monitoring:
        console.print(f"  • {item}")
    console.print()

    # Print summary analysis
    console.print(
        Panel(
            result.summary_analysis,
            title="Analysis Summary",
            border_style="magenta",
        )
    )

    # Clinical notes
    console.print(
        Panel(
            result.clinical_notes,
            title="Clinical Notes",
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
    Main entry point for the similar drugs CLI.

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    parser = create_cli_parser()
    args = parser.parse_args()

    try:
        # Create configuration
        config = SimilarDrugsConfig(
            output_path=args.output if hasattr(args, 'output') else None,
            verbosity=args.verbosity,
        )

        logger.info(f"Configuration created successfully")

        # Run analysis
        model_config = ModelConfig(model="ollama/gemma2", temperature=0.7)
        analyzer = SimilarDrugs(config, model_config)
        result = analyzer.find(
            medicine_name=args.medicine_name,
            include_generics=args.include_generics if hasattr(args, 'include_generics') else True,
            patient_age=args.age if hasattr(args, 'age') else None,
            patient_conditions=args.conditions if hasattr(args, 'conditions') else None,
        )

        # Print results
        print_result(result, verbose=args.verbosity >= 3)

        # Save results to file
        if args.output:
            output_path = args.output
        else:
            medicine_clean = args.medicine_name.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine_clean}_similar_medicines.json"

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
