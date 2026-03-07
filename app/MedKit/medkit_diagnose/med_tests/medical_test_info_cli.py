"""medical_test_info_cli.py - Generate comprehensive medical test information."""

import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging
from medical_test_info import MedicalTestInfoGenerator
from tqdm import tqdm

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical test information."
    )
    parser.add_argument(
        "test",
        type=str,
        help="Medical test name or path to a file containing test names (one per line).",
    )

    # Common user arguments...
    parser.add_argument(
        "-d",
        "--output-dir",
        default="outputs",
        help="Directory for output files (default: outputs).",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="ollama/gemma3",
        help="Model to use for generation (default: ollama/gemma3).",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2).",
    )
    parser.add_argument(
        "-s",
        "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response.",
    )

    return parser.parse_args()


def create_medical_test_info_report(args) -> int:
    """Generate medical test information."""
    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "medical_test_info.log"),
        verbosity=args.verbosity,
        enable_console=True,
    )

    # Determine tests to process
    test_input = Path(args.test)
    if test_input.is_file():
        logger.info(f"Reading test names from file: {args.test}")
        with open(test_input, "r") as f:
            tests = [line.strip() for line in f if line.strip()]
    else:
        tests = [args.test]

    if not tests:
        logger.error("No medical tests provided to process.")
        return 1

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    exit_code = 0
    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedicalTestInfoGenerator(model_config)

        # Use tqdm for a progress bar
        pbar = tqdm(
            tests, desc="Processing medical tests", unit="test", disable=len(tests) <= 1
        )
        for test_name in pbar:
            pbar.set_description(f"Processing: {test_name}")
            logger.info(f"Generating medical test information for: {test_name}")
            result = generator.generate_text(test_name, structured=args.structured)

            if result is None:
                logger.error(f"✗ Failed to generate information for: {test_name}")
                exit_code = 1
                continue

            # Save result to output directory
            saved_path = generator.save(result, output_dir)
            logger.info(f"✓ Medical test information saved to: {saved_path}")

        return exit_code
    except Exception as e:
        logger.error(f"✗ Medical test information generation failed: {e}")
        logger.exception("Full exception details:")
        return 1


def main():
    args = get_user_arguments()
    create_medical_test_info_report(args)


if __name__ == "__main__":
    main()
