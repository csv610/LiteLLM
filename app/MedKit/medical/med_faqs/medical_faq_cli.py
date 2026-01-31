"""Medical FAQ Generator CLI Module.

Generate comprehensive, patient-friendly FAQs for medical topics using structured
data models and the LiteClient with schema-aware prompting for clinical reference
and patient education purposes.
"""

import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging

from medical_faq import MedicalFAQGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical FAQs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medical_faq_cli.py -i diabetes
  python medical_faq_cli.py -i "heart disease" -o output.json -v 3
  python medical_faq_cli.py -i hypertension -d outputs/faq -s
        """
    )
    parser.add_argument(
        "-i", "--topic",
        required=True,
        help="The name of the medical topic to generate FAQs for"
    )
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

    return parser.parse_args()


def create_medical_faq_report(args) -> int:
    """Generate medical FAQ report."""
    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "medical_faq.log"),
        verbosity=args.verbosity,
        enable_console=True
    )
    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Topic: {args.topic}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedicalFAQGenerator(model_config)
        
        faq_info = generator.generate_text(topic=args.topic, structured=args.structured)

        if faq_info is None:
            logger.error("✗ Failed to generate medical FAQ information.")
            return 1

        # Save result to output directory
        generator.save(faq_info, output_dir)

        logger.debug("✓ Medical FAQ generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Medical FAQ generation failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    args = get_user_arguments()
    create_medical_faq_report(args)
