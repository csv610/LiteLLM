import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging

from organ_disease_info import DiseaseInfoGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive disease information based on an organ.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "-i", "--organ",
        required=True,
        help="The name of the organ to list diseases for."
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


def create_disease_info_report(args) -> int:
    """Generate disease information report."""
    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "disease_info.log"),
        verbosity=args.verbosity,
        enable_console=True
    )
    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Organ: {args.organ}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = DiseaseInfoGenerator(model_config)
        
        logger.debug(f"  Organ: {args.organ}")
        result = generator.generate_text(organ=args.organ, structured=args.structured)

        if result is None:
            logger.error("✗ Failed to generate disease information.")
            return 1

        # Save result to output directory
        generator.save(result, output_dir)

        logger.debug("✓ Information generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Disease information generation failed: {e}")
        logger.exception("Full exception details:")
        return 1


def main():
    """Main entry point for the CLI."""
    args = get_user_arguments()
    create_disease_info_report(args)


if __name__ == "__main__":
    main()
