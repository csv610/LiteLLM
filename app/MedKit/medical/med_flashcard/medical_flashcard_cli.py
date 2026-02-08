import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging

from medical_flashcard import MedicalFlashcardGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate medical flashcard reports from images.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # Primary positional argument: Image path
    parser.add_argument(
        "image",
        help="Path to an image of the medical flashcard."
    )
    parser.add_argument(
        "pos_model",
        nargs="?",
        help="Model to use for generation (positional)."
    )
    
    # Optional flags
    parser.add_argument(
        "-d", "--output-dir",
        default="outputs",
        help="Directory for output files (default: outputs)."
    )
    parser.add_argument(
        "-m", "--model",
        default="ollama/gemma3:27b-cloud",
        help="Model to use for generation (flag)."
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Use quick mode (no Pydantic model for response formatting)."
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

    args = parser.parse_args()

    return args


def create_medical_flashcard_report(args) -> int:

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "medical_flashcard.log"),
        verbosity=args.verbosity,
        enable_console=True
    )
    
    logger.debug(f"  Image: {args.image}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedicalFlashcardGenerator(model_config)
        
        # Determine if structured output should be used
        use_structured = args.structured and not args.quick
        
        # In this workflow, the user ONLY provides an image.
        # We first extract terms and then explain them via generate_text.
        logger.info(f"Processing image: {args.image}")
        results = generator.generate_text(
            image_path=args.image, 
            structured=use_structured
        )
        
        if not results:
            logger.error("✗ No medical terms could be extracted or processed from the image.")
            return 1
        
        for term, flashcard_info in results:
            logger.info(f"Saving report for: {term}")
            generator.save(flashcard_info, output_dir, term=term)

        logger.debug("Medical flashcard processing completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Medical flashcard processing failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    args = get_user_arguments()
    create_medical_flashcard_report(args)
