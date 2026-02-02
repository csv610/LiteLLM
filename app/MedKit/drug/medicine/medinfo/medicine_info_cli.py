"""Medicine Information CLI Module.

This module provides a command-line interface for generating comprehensive
medicine information using AI-powered analysis.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Union

from lite.config import ModelConfig
from lite.logging_config import configure_logging

from medicine_info import MedicineInfoGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive medicine information using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "medicine",
        type=str,
        help="Medicine name (e.g., 'Aspirin', 'Ibuprofen')"
    )

    parser.add_argument(
        "-d", "--output-dir",
        type=str,
        default="outputs",
        help="Directory for output files (default: outputs)"
    )

    parser.add_argument(
        "-m", "--model",
        type=str,
        default="ollama/gemma3",
        help="LLM model to use (default: ollama/gemma3)"
    )

    parser.add_argument(
        "-v", "--verbosity",
        type=int,
        default=2,
        help="Logging verbosity level (0-4) (default: 2)"
    )

    parser.add_argument(
        "-s", "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model)"
    )

    return parser.parse_args()


def create_medicine_info_report(args) -> int:
    """Create and save medicine information report.

    Args:
        args: Parsed command-line arguments

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    # Ensure logs directory exists
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    # Apply logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "medicine_info.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.info("="*80)
    logger.info("MEDICINE INFO CLI - Starting")
    logger.info("="*80)

    # Determine output directory and base filename FIRST (fail-fast validation)
    output_dir = Path(args.output_dir)
    base_filename = f"{args.medicine.lower().replace(' ', '_')}"
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedicineInfoGenerator(model_config)

        # Generate the medicine information (expensive operation)
        result = generator.generate_text(args.medicine, structured=args.structured)
        
        # Save results
        saved_path = generator.save(result, output_dir / base_filename)
        logger.info(f"✓ Medicine information saved to: {saved_path}")
        print(f"✓ Report saved to: {saved_path}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Critical error during CLI execution: {e}", exc_info=True)
        return 1


def main():
    args = get_user_arguments()
    create_medicine_info_report(args)

if __name__ == "__main__":
   main()
