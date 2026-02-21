"""medical_test_info_cli.py - Generate comprehensive medical test information."""

import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging

from medical_test_info import MedicalTestInfoGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Generate comprehensive medical test information.")
    parser.add_argument("-i", "--test", type=str, required=True, help="The name of the medical test to generate information for.")
    parser.add_argument("-d", "--output-dir", default="outputs", help="Directory for output files (default: outputs).")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use for generation (default: ollama/gemma3).")
    parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2).")
    parser.add_argument("-s", "--structured", action="store_true", default=False, help="Use structured output (Pydantic model) for the response.")

    return parser.parse_args()


def create_medical_test_info_report(args) -> int:
    """Generate medical test information."""
    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "medical_test_info.log"),
        verbosity=args.verbosity,
        enable_console=True
    )
    logger.info(f"Generating medical test information for: {args.test}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedicalTestInfoGenerator(model_config)
        
        result = generator.generate_text(args.test, structured=args.structured)

        if result is None:
            logger.error("✗ Failed to generate medical test information.")
            return 1

        # Save result to output directory
        saved_path = generator.save(result, output_dir)
        logger.info(f"✓ Medical test information saved to: {saved_path}")
        return 0
    except Exception as e:
        logger.error(f"✗ Medical test information generation failed: {e}")
        logger.exception("Full exception details:")
        return 1


def main():
    args = get_user_arguments()
    create_medical_test_info_report(args)

if __name__ == "__main__":
   main()
