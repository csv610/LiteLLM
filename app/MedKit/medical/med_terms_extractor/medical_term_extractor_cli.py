"""medical_term_extractor.py - Extract and categorize medical concepts from text."""

import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging

from medical_term_extractor import MedicalTermExtractor

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Extract medical terms from text or a file.")
    parser.add_argument("input", help="The input text file path or a string of text.")
    parser.add_argument("-d", "--output-dir", default="outputs", help="Directory for output files (default: outputs).")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use (default: ollama/gemma3).")
    parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2).")
    parser.add_argument("-s", "--structured", action="store_true", default=False, help="Use structured output (Pydantic model) for the response.")

    return parser.parse_args()


def create_medical_term_extractor_report(args) -> int:
    """Extract medical terms from text or file."""
    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "medical_term_extractor.log"),
        verbosity=args.verbosity,
        enable_console=True
    )
    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Input: {args.input}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.1)
        extractor = MedicalTermExtractor(model_config)
        
        # Handle input - check if it's a file or direct text
        input_text = args.input
        input_path = Path(args.input)
        if input_path.is_file():
            with open(input_path, 'r', encoding='utf-8') as f:
                input_text = f.read()
            logger.debug(f"Read input from file: {input_path}")
        else:
            logger.debug(f"Using direct text input")

        terms_info = extractor.generate_text(input_text, structured=args.structured)

        if terms_info is None:
            logger.error("✗ Failed to extract medical terms.")
            return 1

        # Save result to output directory
        extractor.save(terms_info, output_dir)

        logger.debug("✓ Medical term extraction completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Medical term extraction failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    args = get_user_arguments()
    create_medical_term_extractor_report(args)
