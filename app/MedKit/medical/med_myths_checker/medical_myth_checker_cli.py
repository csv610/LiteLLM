"""Medical Myths Checker - Comprehensive analysis of medical myths and claims."""

import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging

from medical_myth_checker import MedicalMythsChecker
from medical_myth_checker_models import MedicalMythAnalysisModel
from medical_myth_checker_prompts import PromptBuilder

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyze medical myths and provide evidence-based assessments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Medical myth/claim to analyze"
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


def create_medical_myth_report( args) -> int:

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "medical_myths_checker.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.info("="*80)
    logger.info("MEDICAL MYTHS CHECKER CLI - Starting")
    logger.info("="*80)

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        checker = MedicalMythsChecker(model_config=model_config)
        
        result = checker.generate_text(myth=args.input, structured=args.structured)

        if result is None:
            logger.error("✗ Failed to analyze medical myth.")
            return 1

        # Save result to output directory
        checker.save(result, output_dir)

        logger.debug("✓ Medical myth analysis completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Medical myth analysis failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == '__main__':
    args = get_user_arguments()
    create_medical_myth_report(args)
