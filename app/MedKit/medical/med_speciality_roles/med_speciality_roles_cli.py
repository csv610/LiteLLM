import argparse
import logging
import sys
from pathlib import Path

# Add project root to sys.path

from lite.config import ModelConfig
from lite.logging_config import configure_logging
from lite.utils import save_model_response
from med_speciality_roles import MedSpecialityRoles

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Get roles and responsibilities of a medical specialist.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-s", "--speciality",
        required=True,
        help="The medical speciality to query (e.g., 'Cardiologist')."
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


def get_speciality_roles(args) -> int:
    """Generate speciality roles description."""
    # Ensure logs directory exists
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Apply verbosity using centralized logging configuration
    configure_logging(
        log_file=str(log_dir / "med_speciality_roles.log"),
        verbosity=args.verbosity,
        enable_console=True
    )
    
    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Speciality: {args.speciality}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Model: {args.model}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.0)
        med_roles = MedSpecialityRoles(model_config)
        
        result = med_roles.generate_text(args.speciality)
        
        if not result or result.startswith("Error"):
             logger.error(f"✗ Failed to generate roles: {result}")
             return 1

        print(result)
        logger.debug("✓ Roles retrieved successfully")
        
        return 0
    except Exception as e:
        logger.error(f"✗ Role retrieval process failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    args = get_user_arguments()
    sys.exit(get_speciality_roles(args))
