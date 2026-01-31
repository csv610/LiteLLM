import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging

from herbal_info import HerbalInfoGenerator

logger = logging.getLogger(__name__)

def add_common_arguments(parser):
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

def get_user_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive herbal information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python herbal_info_cli.py -i ginger
  python herbal_info_cli.py -i "echinacea" -o output.json -v 3
  python herbal_info_cli.py -i turmeric -d outputs/herbs
        """
    )
    parser.add_argument(
        "-i", "--herb",
        required=True,
        help="The name of the herb to generate information for."
    )
    add_common_arguments(parser)
    return parser.parse_args()

def create_herbal_info_report(args):

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "herbal_info.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Herb: {args.herb}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate herbal information
    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = HerbalInfoGenerator(model_config)
        result    = generator.generate_text(herb=args.herb, structured=args.structured)

        if result is None:
            logger.error("✗ Failed to generate herbal information.")
            return 1

        # Save result to output directory
        generator.save(result, output_dir)

        logger.debug("✓ Herbal information generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Herbal information generation failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    args = get_user_arguments()
    create_herbal_info_report(args)
