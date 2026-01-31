"""Module docstring - Medical Anatomy Information Generator.

Generate comprehensive, evidence-based anatomical information using structured
data models and the LiteClient with schema-aware prompting for clinical reference
and education purposes.
"""

import argparse
import json
import logging
import sys
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging

from medical_anatomy import MedicalAnatomyGenerator

logger = logging.getLogger(__name__)

def common_user_arguments(parser):

    parser.add_argument(
        "-d", "--output-dir",
        default="outputs",
        help="Directory for output files (default: outputs)."
    )

    parser.add_argument(
        "-m", "--model",
        default="ollama/gemma3",
        help="Model to use for generation (default: ollama/gemma3)."
    )

    parser.add_argument(
        "-v", "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2)."
    )

    parser.add_argument(
        "-s", "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response."
    )

def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical anatomy information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    common_user_arguments(parser)

    parser.add_argument(
        "-i", "--body_part",
        required=True,
        help="The name of the anatomical part  to generate information for."
    )

    return parser.parse_args()


def create_medical_anatomy_report(args):
    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "medical_anatomy.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate anatomical information
    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedicalAnatomyGenerator(model_config)
        result = generator.generate_text(body_part=args.body_part, structured=args.structured)

        if result is None:
            logger.error("✗ Failed to generate anatomical information.")
            sys.exit(1)

        # Save result to output directory
        generator.save(result, output_dir)

        logger.debug("✓ Anatomical information generation completed successfully")
        return 
    except Exception as e:
        logger.error(f"✗ Anatomical information generation failed: {e}")
        logger.exception("Full exception details:")
        sys.exit(1)


if __name__ == "__main__":
    args = get_user_arguments()
    create_medical_anatomy_report(args)
