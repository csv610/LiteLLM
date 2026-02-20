"""
faq_generator_cli.py - CLI interface for FAQ generation

Contains command-line interface functions for the FAQ generator,
including argument parsing, validation, and main entry point.
"""

import argparse
import logging
import json
import sys
import os
from pathlib import Path

from lite import ModelConfig
from lite.logging_config import configure_logging
from faq_generator import FAQGenerator, FAQInput
from faq_generator_models import VALID_DIFFICULTIES

# Global logger for the application
logger = logging.getLogger(__name__)


def validate_num_faqs(num_str: str) -> int:
    """
    Validate number of FAQs is in valid range.

    Args:
        num_str: Number as string

    Returns:
        Validated integer

    Raises:
        argparse.ArgumentTypeError: If invalid
    """
    try:
        num = int(num_str)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Must be an integer, got '{num_str}'")

    if num < 1 or num > 100:
        raise argparse.ArgumentTypeError(
            f"Must be between 1-100, got {num}"
        )
    return num


def validate_input_source(source_str: str) -> str:
    """
    Validate input source (file path or topic string).

    Args:
        source_str: Input source to validate

    Returns:
        Validated input source

    Raises:
        argparse.ArgumentTypeError: If invalid
    """
    if not source_str or not source_str.strip():
        raise argparse.ArgumentTypeError("Input source cannot be empty")

    source_str = source_str.strip()

    # If file exists, accept it
    if os.path.exists(source_str):
        return source_str

    # Otherwise validate as topic string
    if len(source_str) < 2 or len(source_str) > 100:
        raise argparse.ArgumentTypeError(
            "Topic must be 2-100 characters (or provide valid file path)"
        )
    return source_str


def validate_difficulty(difficulty_str: str) -> str:
    """
    Validate difficulty level.

    Args:
        difficulty_str: Difficulty level

    Returns:
        Normalized difficulty level

    Raises:
        argparse.ArgumentTypeError: If invalid
    """
    difficulty = difficulty_str.lower().strip()
    if difficulty not in VALID_DIFFICULTIES:
        raise argparse.ArgumentTypeError(
            f"Must be: {', '.join(VALID_DIFFICULTIES)}, got '{difficulty_str}'"
        )
    return difficulty


def arguments_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    
    parser = argparse.ArgumentParser(
        description="Generate frequently asked questions on a given topic or from content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate FAQs from topic
  python faq_generator_cli.py -i "Python Programming" -n 10 -d simple
  python faq_generator_cli.py --input "Machine Learning" --num-faqs 5 --difficulty hard
  python faq_generator_cli.py -i "Web Development" -n 8 -d medium -m claude-3-opus

  # Generate FAQs from content file
  python faq_generator_cli.py -i content.txt -n 5 -d research
  python faq_generator_cli.py --input article.md --num-faqs 10 --difficulty medium
        """
    )

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        type=validate_input_source,
        dest="input_source",
        help="Input source: topic string (2-100 chars) or path to content file (txt, md, etc). "
             "If a file path exists, file is processed; otherwise treated as topic string"
    )

    parser.add_argument(
        "-n",
        "--num-faqs",
        default=5,
        type=validate_num_faqs,
        dest="num_faqs",
        help="Number of FAQs to generate (1-100). Determines how many question-answer pairs to create"
    )

    parser.add_argument(
        "-d",
        "--difficulty",
        required=False,
        default="medium",
        type=validate_difficulty,
        dest="difficulty",
        choices=VALID_DIFFICULTIES,
        help="Difficulty level: simple (beginner-friendly), medium (intermediate, practical), "
             "hard (advanced, specialized knowledge), research (cutting-edge, open problems). "
             "Default: medium"
    )

    parser.add_argument(
        "-m",
        "--model",
        default=None,
        dest="model",
        help="LLM model identifier in format 'provider/model' (e.g., 'ollama/gemma3', 'gpt-4', 'claude-3-opus'). "
             "Default: ollama/gemma3"
    )

    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        default=0.3,
        dest="temperature",
        help="Sampling temperature controlling output randomness (0.0-2.0). Lower values = more deterministic. "
             "Default: 0.3"
    )

    parser.add_argument(
        "-o",
        "--output",
        default=".",
        dest="output_dir",
        help="Output directory path for saving FAQ JSON file. Directory must exist. Default: current directory"
    )

    return parser


def main() -> int:
    """
    Main entry point for FAQ generator CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    global logger
    
    parser = arguments_parser()
    args = parser.parse_args()

    try:
        # Initialize global logger
        configure_logging(log_file=str(Path(__file__).parent / "logs" / "faq_generator.log"))
        
        # Create ModelConfig
        model_config = ModelConfig(model=args.model, temperature=args.temperature)
        
        # Create FAQInput
        faq_input = FAQInput(
            input_source=args.input_source,
            num_faqs=args.num_faqs,
            difficulty=args.difficulty,
            output_dir=args.output_dir
        )
        
        # Initialize generator with ModelConfig
        generator = FAQGenerator(model_config)

        # Determine source type
        source_type = "file" if os.path.exists(args.input_source) else "topic"
        print(f"Generating {args.num_faqs} {args.difficulty} FAQs from {source_type} '{args.input_source}'...")

        # Generate FAQs
        faqs = generator.generate_text(faq_input)

        if not faqs:
            logger.error("No FAQs returned from API")
            return 1

        # Save to file
        output_file = generator.save_to_file(faqs, faq_input)

        print(f"FAQ generation complete. Saved to {output_file}")
        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        if logger: logger.error(f"ValueError: {e}")
        return 1
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        if logger: logger.error(f"RuntimeError: {e}")
        return 1
    except IOError as e:
        print(f"Error: {e}", file=sys.stderr)
        if logger: logger.error(f"IOError: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if logger: logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
