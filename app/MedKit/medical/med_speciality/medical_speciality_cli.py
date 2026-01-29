"""medical_speciality_cli.py - CLI for Medical Specialists Database and Lookup"""

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.config import ModelConfig
from lite.logging_config import configure_logging

from medical_speciality import MedicalSpecialityGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Generate comprehensive medical specialist database")
    parser.add_argument("-d", "--output-dir", default="outputs", help="Directory for output files (default: outputs).")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use (default: ollama/gemma3).")
    parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2).")
    parser.add_argument("-s", "--structured", action="store_true", default=False, help="Use structured output (Pydantic model) for the response.")

    return parser.parse_args()


def create_medical_speciality_report(args) -> int:
    """Generate medical speciality database."""
    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "medical_speciality.log"),
        verbosity=args.verbosity,
        enable_console=True
    )
    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        generator = MedicalSpecialityGenerator(model_config)
        
        speciality_info = generator.generate_text(structured=args.structured)

        if speciality_info is None:
            logger.error("✗ Failed to generate medical speciality database.")
            return 1

        # Save result to output directory
        generator.save(speciality_info, output_dir)

        logger.debug("✓ Medical speciality database generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Medical speciality database generation failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    args = get_user_arguments()
    create_medical_speciality_report(args)
