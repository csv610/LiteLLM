import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging

from primary_health_care import PrimaryHealthCareProvider

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Ask a question to a Primary Health Care Provider.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-q", "--query",
        required=True,
        help="The health concern or question you want to ask."
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


def main():
    args = get_user_arguments()

    # Ensure logs directory exists
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(log_dir / "primary_health_care.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.info("="*80)
    logger.info("PRIMARY HEALTH CARE PROVIDER - Starting")
    logger.info("="*80)

    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Query: {args.query}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        provider = PrimaryHealthCareProvider(model_config)
        response = provider.generate_text(query=args.query, structured=args.structured)

        if response is None:
            logger.error("✗ Failed to generate a response.")
            return 1

        # Save result to output directory
        saved_path = provider.save(response, output_dir)
        
        logger.info(f"✓ Response saved to: {saved_path}")
        
        # Also print markdown output to console if available
        if response.markdown:
            print("\n--- Provider Response ---\n")
            print(response.markdown)
            print("\n--------------------------\n")

        logger.debug("✓ Primary health care interaction completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Primary health care interaction failed: {e}")
        logger.exception("Full exception details:")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
