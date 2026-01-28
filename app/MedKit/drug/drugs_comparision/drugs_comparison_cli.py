"""Module docstring - Medicines Comparison Tool.

Compare medicines side-by-side across clinical, regulatory, and practical metrics to help
healthcare professionals and patients make informed treatment decisions.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional, Union


sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging

from drugs_comparison_models import MedicinesComparisonResult
from drugs_comparison import DrugsComparison, DrugsComparisonInput
from drugs_comparison_prompts import PromptBuilder

logger = logging.getLogger(__name__)


def get_user_arguments():
    """Create and configure the argument parser for the CLI."""
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

  # With custom model and JSON output
  python drugs_comparison.py "Atorvastatin" "Simvastatin" --model "ollama/llama3" --json-output
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
        "--model",
        "-m",
        type=str,
        default="ollama/gemma2",
        help="Model ID to use for the comparison (e.g., 'ollama/llama3', 'openai/gpt-4o')",
    )

    parser.add_argument(
        "--json-output",
        "-j",
        action="store_true",
        default=False,
        help="Output results as JSON to stdout",
    )

    parser.add_argument(
        "-s", "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response."
    )

    parser.add_argument(
        "-d", "--output-dir",
        default="outputs",
        help="Directory for output files (default: outputs)."
    )

    return parser.parse_args()

def create_drugs_comparision_report(args) -> int:

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "drugs_comparison.log"),
        verbosity=args.verbosity,
        enable_console=True
    )
    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Medicine 1: {args.medicine1}")
    logger.debug(f"  Medicine 2: {args.medicine2}")
    logger.debug(f"  Use Case: {args.use_case}")
    logger.debug(f"  Age: {args.age}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Create configuration
        config = DrugsComparisonInput(
            medicine1=args.medicine1,
            medicine2=args.medicine2,
            use_case=args.use_case,
            patient_age=args.age,
            patient_conditions=args.conditions,
            prompt_style=args.prompt_style,
        )

        # Run analysis
        model_config = ModelConfig(model=args.model, temperature=0.7)
        analyzer = DrugsComparison(model_config)
        result = analyzer.generate_text(config, structured=args.structured)

        if result is None:
            logger.error("✗ Failed to generate drugs comparison information.")
            return 1

        # Save result to output directory
        analyzer.save(result, output_dir)

        logger.debug("✓ Drugs comparison generation completed successfully")
        return 0

    except ValueError as e:
        print(f"\n❌ Invalid input: {e}")
        logger.error(f"Invalid input: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"Unexpected error: {e}")
        logger.exception("Full exception details:")
        return 1



if __name__ == "__main__":
    args = get_user_arguments()
    create_drugs_comparision_report(args)
