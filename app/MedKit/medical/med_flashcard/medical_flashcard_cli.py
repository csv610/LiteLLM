import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging
from lite.lite_client import LiteClient

from medical_flashcard import MedicalLabelExtractor, MedicalTermExplainer

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Explain medical labels extracted from images.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # Primary positional argument: Image path
    parser.add_argument(
        "image",
        help="Path to an image containing medical labels."
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
        "-m1", "--extractor-model",
        help="Model to use for extraction (defaults to --model if not specified)."
    )
    parser.add_argument(
        "-m2", "--explainer-model",
        help="Model to use for explanation (defaults to --model if not specified)."
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
        # Determine which model to use as default
        default_model = args.pos_model if args.pos_model else args.model
        
        model = args.extractor_model if args.extractor_model else default_model
        model_config = ModelConfig(model=model, temperature=0.5)
        extractor = MedicalLabelExtractor(model_config)

        # In this workflow, the user ONLY provides an image.
        # We first extract terms and then explain them.
        logger.info(f"Processing image: {args.image}")
        terms = extractor.extract_terms(args.image)

        for idx, term in enumerate(terms):
            print(idx+1, term)

        return 0
        
        if not terms:
            logger.error("✗ No medical terms could be extracted from the image.")
            return 1


        # Initialize the explainer with the specified or default model
        explainer_model_name = args.explainer_model if args.explainer_model else default_model
        explainer_config = ModelConfig(model=explainer_model_name, temperature=0.2)
        explainer = MedicalTermExplainer(explainer_config)

        # Determine if structured output should be used
        use_structured = args.structured and not args.quick
        
        logger.info(f"Generating explanations for {len(terms)} terms...")
        results = explainer.explain_terms(terms, structured=use_structured)
        
        for term, flashcard_info in results:
            logger.info(f"Saving report for: {term}")
            explainer.save(flashcard_info, output_dir, term=term)

        logger.info("✓ Medical flashcard processing completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Medical flashcard processing failed: {e}")
        logger.exception("Full exception details:")
        return 1


def main():
    args = get_user_arguments()
    create_medical_flashcard_report(args)

if __name__ == "__main__":
   main()
