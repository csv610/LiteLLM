import argparse
import logging
import sys
from pathlib import Path

# Add project root to sys.path

from lite.config import ModelConfig
from lite.logging_config import configure_logging
from lite.utils import save_model_response
from med_refer import MedReferral

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Recommend medical specialists based on symptoms.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medrefer_cli.py -i "I have a headache"
        """
    )
    parser.add_argument(
        "-i", "--question",
        required=True,
        help="The medical question or symptoms."
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

    return parser.parse_args()


def create_referral_recommendation(args) -> int:
    """Generate specialist recommendation."""
    # Ensure logs directory exists
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Apply verbosity using centralized logging configuration
    configure_logging(
        log_file=str(log_dir / "med_refer.log"),
        verbosity=args.verbosity,
        enable_console=True
    )
    
    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Question: {args.question}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Model: {args.model}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.0)
        med_referral = MedReferral(model_config)
        
        result  = med_referral.generate_text(args.question)
        
        if not result or result.startswith("Error"):
             logger.error(f"✗ Failed to generate recommendation: {result}")
             return 1

        print(result)
        logger.debug("✓ Recommendation saved successfully")
        
        return 0
    except Exception as e:
        logger.error(f"✗ Referral process failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    args = get_user_arguments()
    sys.exit(create_referral_recommendation(args))
