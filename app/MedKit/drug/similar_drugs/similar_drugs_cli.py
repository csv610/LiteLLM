"""Module docstring - Similar Medicines Finder and Comparator.

Find alternative medicines with similar active ingredients, therapeutic classes, and
mechanisms of action. Provides detailed comparisons to help identify suitable substitutes.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Union

from lite.config import ModelConfig
from lite.logging_config import configure_logging

from similar_drugs_models import SimilarMedicinesResult
from similar_drugs import SimilarDrugs

logger = logging.getLogger(__name__)

@dataclass
class SimilarDrugsConfig:
    """Configuration for finding similar drugs."""
    output_path: Optional[Path] = None
    verbosity: int = 2  # 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG
    enable_cache: bool = True


def get_similar_medicines(
    medicine_name: str,
    config: SimilarDrugsConfig,
    model_config: ModelConfig,
    include_generics: bool = True,
    patient_age: Optional[int] = None,
    patient_conditions: Optional[str] = None,
    structured: bool = False,
) -> Union[SimilarMedicinesResult, str]:
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
        structured=structured,
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
        "-s", "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response."
    )

    return parser

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

        logger.debug(f"Configuration created successfully")

        # Run analysis
        model_config = ModelConfig(model="ollama/gemma2", temperature=0.7)
        analyzer = SimilarDrugs(config, model_config)
        result = analyzer.find(
            medicine_name=args.medicine_name,
            include_generics=args.include_generics if hasattr(args, 'include_generics') else True,
            patient_age=args.age if hasattr(args, 'age') else None,
            patient_conditions=args.conditions if hasattr(args, 'conditions') else None,
            structured=args.structured,
        )

        # Save results to file
        if args.output:
            output_path = args.output
        else:
            medicine_clean = args.medicine_name.lower().replace(' ', '_')
            suffix = ".json"
            if isinstance(result, str):
                suffix = ".md"
            output_path = Path("outputs") / f"{medicine_clean}_similar_medicines{suffix}"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(result, str) and output_path.suffix == ".json":
            output_path = output_path.with_suffix(".md")

        with open(output_path, "w") as f:
            if isinstance(result, str):
                f.write(result)
            else:
                f.write(result.model_dump_json(indent=2))

        logger.debug(f"✓ Results saved to {output_path}")
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
        return 1

if __name__ == "__main__":
    sys.exit(main())
