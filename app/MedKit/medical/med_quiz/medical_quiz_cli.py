"""Medical Quiz Generator CLI Module.

Generate comprehensive medical quizzes using structured
data models and the LiteClient with schema-aware prompting for clinical
reference and medical education purposes.
"""

import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging

from medical_quiz import MedicalQuizGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical Quizzes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medical_quiz_cli.py -i diabetes
  python medical_quiz_cli.py -i "heart disease" --difficulty Hard --num-questions 10
  python medical_quiz_cli.py -i hypertension -s --num-options 5
        """
    )
    parser.add_argument(
        "-i", "--topic",
        required=True,
        help="The name of the medical topic to generate a quiz for"
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
    parser.add_argument(
        "--difficulty", "-df",
        default="Intermediate",
        help="Difficulty level for quiz (default: Intermediate)."
    )
    parser.add_argument(
        "--num-questions", "-nq",
        type=int,
        default=5,
        help="Number of questions for quiz (default: 5)."
    )
    parser.add_argument(
        "--num-options", "-no",
        type=int,
        default=4,
        help="Number of options for each quiz question (default: 4)."
    )

    return parser.parse_args()


def create_medical_quiz(args) -> int:
    """Generate medical quiz."""
    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "medical_content.log"),
        verbosity=args.verbosity,
        enable_console=True
    )
    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Topic: {args.topic}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    logger.info(f"Generating medical quiz information for: {args.topic}")

    try:
        # Create model configuration
        model_config = ModelConfig(
            model=args.model,
            temperature=0.7
        )

        # Initialize the generator
        generator = MedicalQuizGenerator(model_config)

        # Always use structured output internally for proper formatting
        # The user doesn't need to specify -s flag - we handle it automatically
        logger.info("Generating quiz with automatic formatting...")
        result = generator.generate_text(
            topic=args.topic,
            difficulty=args.difficulty,
            num_questions=args.num_questions,
            num_options=args.num_options,
            structured=True  # Always use structured for proper formatting
        )

        # Save the result
        output_path = generator.save(result, Path(args.output_dir))
        logger.info(f"✓ Medical quiz generation completed successfully")
        logger.info(f"✓ Output saved to: {output_path}")
        return 0

    except Exception as e:
        logger.error(f"✗ Medical quiz generation failed: {e}")
        logger.error(f"Full exception details: {e}")
        return 1


if __name__ == "__main__":
    args = get_user_arguments()
    create_medical_quiz(args)
