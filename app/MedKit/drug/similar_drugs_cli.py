"""
similar_drugs.py - Similar Medicines Finder and Comparator

Find alternative medicines with similar active ingredients, therapeutic classes, and
mechanisms of action. Provides detailed comparisons of top 10-15 alternatives to help
identify suitable substitutes using structured data and MedKit AI analysis.

This module helps identify appropriate alternative medications when the primary drug is
unavailable, contraindicated, or causing adverse effects.

QUICK START:
    from similar_drugs import SimilarDrugs, SimilarDrugsConfig

    # Configure the analysis (settings only)
    config = SimilarDrugsConfig(
        output_path=None,  # optional
        verbosity=False,
        prompt_style="DETAILED"
    )

    # Create an analyzer and get the alternatives
    alternatives = SimilarDrugs(config).find(
        medicine_name="ibuprofen",
        include_generics=True
    )

    # Review similar options
    for category in alternatives.categorized_results:
        for drug in category.medicines[:3]:
            print(f"{drug.medicine_name}: {drug.similarity_category.value}")
            print(f"  Efficacy: {drug.efficacy_comparison.value}")

COMMON USES:
    1. Find alternative medications when primary drug is unavailable
    2. Identify options when patient has contraindications
    3. Compare efficacy and side effects of similar drugs
    4. Support medication selection decisions
    5. Generate patient education on medication alternatives
    6. Manage drug allergies with suitable substitutes

SIMILARITY BASIS:
    - SAME_INGREDIENT: Contains the same active ingredient
    - SAME_THERAPEUTIC_CLASS: Treats the same conditions similarly
    - SIMILAR_MECHANISM: Works through similar pharmacological mechanisms

KEY INFORMATION PROVIDED:
    - Alternative medicine names
    - Similarity basis and strength
    - Efficacy comparison to original drug
    - Availability and cost considerations
    - Substitutability rating
    - Important considerations for switching
"""

import logging
import sys
import json
import argparse
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from medkit.core.medkit_client import MedKitClient, MedKitConfig
from medkit.utils.pydantic_prompt_generator import PromptStyle
from medkit.utils.logging_config import setup_logger

from similar_drugs_models import (
    SimilarityCategory,
    EfficacyComparison,
    SimilarMedicineDetail,
    SimilarMedicinesCategory,
    SwitchingGuidance,
    SimilarMedicinesResult,
)

# Configure logging
logger = setup_logger(__name__)
logger.info("="*80)
logger.info("Similar Drugs Module Initialized")
logger.info("="*80)


@dataclass
class SimilarDrugsConfig(MedKitConfig):
    """
    Configuration for similar_drugs.

    Inherits from StorageConfig for LMDB database settings:
    - db_path: Auto-generated path to similar_drugs.lmdb
    - db_capacity_mb: Database capacity (default 500 MB)
    - db_store: Whether to cache results (default True)
    - db_overwrite: Whether to refresh cache (default False)
    """
    """Configuration for finding similar drugs."""
    output_path: Optional[Path] = None
    verbosity: bool = False
    prompt_style: PromptStyle = PromptStyle.DETAILED
    enable_cache: bool = True

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "similar_drugs.lmdb"
            )
        # Call parent validation
        super().__post_init__()

class SimilarDrugs:
    """Finds similar drugs based on provided configuration."""

    def __init__(self, config: SimilarDrugsConfig):
        self.config = config

        # Load model name from ModuleConfig
        model_name = "gemini-1.5-flash"  # Default model for this module

        self.client = MedKitClient(model_name=model_name)

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
            prompt=f"Find the top 10-15 most similar medicines to {medicine_name} - prioritize same active ingredients, then therapeutic class, then similar mechanism. {context}",
            schema=SimilarMedicinesResult,
        )

        return result


def get_similar_medicines(
    medicine_name: str,
    config: SimilarDrugsConfig,
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
        include_generics: Whether to include generic formulations (default: True)
        patient_age: Patient's age in years (optional)
        patient_conditions: Patient's medical conditions (optional)

    Returns:
        SimilarMedicinesResult: The result of the analysis
    """
    finder = SimilarDrugs(config)
    return finder.find(
        medicine_name=medicine_name,
        include_generics=include_generics,
        patient_age=patient_age,
        patient_conditions=patient_conditions,
    )


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

    return parser


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


def print_results(result: SimilarMedicinesResult, verbose: bool = False) -> None:
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


def main() -> int:
    """
    Main entry point for the similar drugs CLI.

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
        # Parse prompt style
        prompt_style = parse_prompt_style(args.prompt_style)

        # Create configuration
        config = SimilarDrugsConfig(
            output_path=args.output,
            verbosity=args.verbose,
            prompt_style=prompt_style,
        )

        logger.info(f"Configuration created successfully")

        # Run analysis
        analyzer = SimilarDrugs(config)
        result = analyzer.find(
            medicine_name=args.medicine_name,
            include_generics=args.include_generics,
            patient_age=args.age,
            patient_conditions=args.conditions,
        )

        # Print results
        print_results(result, verbose=args.verbose)

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


if __name__ == "__main__":
    sys.exit(main())
