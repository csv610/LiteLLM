import argparse
import logging
import json
import sys
import os
import re
from pathlib import Path
from typing import Optional

# Add parent directory to path to import lite module
#sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lite import LiteClient, ModelConfig, configure_logging
from lite.config import ModelInput

from unsolved_problems_models import UnsolvedProblem, UnsolvedProblemsResponse
from unsolved_problems_prompts import PromptBuilder
from unsolved_problems_explorer import UnsolvedProblemsExplorer

configure_logging(log_file=str(Path(__file__).parent / "logs" / "unsolved.log"))
logger = logging.getLogger(__name__)


# ==============================================================================
# Core Functions
# ==============================================================================

def _handle_api_error(error: Exception) -> None:
    """
    Handle and translate API errors to meaningful exceptions.

    Args:
        error: Exception raised during API call

    Raises:
        RuntimeError: With appropriate error message
    """
    error_str = str(error).lower()

    if "401" in str(error) or "authentication" in error_str:
        logger.error("Authentication failed: Check your API credentials")
        raise RuntimeError("API authentication failed. Check LITELLM_API_KEY or model-specific credentials.")
    elif "429" in str(error):
        logger.error("Rate limit exceeded")
        raise RuntimeError("API rate limit exceeded. Please try again later.")
    elif "404" in str(error):
        logger.error("Model not found")
        raise RuntimeError("Model not found or not available.")
    else:
        logger.error(f"Unexpected error: {error}")
        raise RuntimeError(f"Failed to fetch unsolved problems: {error}")


def fetch_unsolved_problems(
    topic: str,
    num_problems: int,
    model: Optional[str] = None
) -> list[UnsolvedProblem]:
    """
    Fetch unsolved problems for a specific topic.

    Args:
        topic: The topic to find unsolved problems for
        num_problems: Number of unsolved problems to retrieve
        model: LLM model to use (defaults to environment variable or ollama/gemma3)

    Returns:
        List of UnsolvedProblem instances

    Raises:
        ValueError: If API response is invalid or model response doesn't match schema
        RuntimeError: If API call fails or required credentials are missing
    """
    # Initialize explorer with specified model
    explorer = UnsolvedProblemsExplorer(model=model)
    
    # Fetch problems using the explorer
    return explorer.fetch_problems(topic, num_problems)


# ==============================================================================
# Validation Functions
# ==============================================================================

def validate_num_problems(num_str: str) -> int:
    """
    Validate and convert number of problems string to integer.

    Args:
        num_str: Number of problems as string

    Returns:
        Number of problems as integer

    Raises:
        argparse.ArgumentTypeError: If number is invalid
    """
    try:
        num = int(num_str)
        if num < 1:
            raise argparse.ArgumentTypeError(
                f"Number of problems must be at least 1, got {num}"
            )
        if num > 50:
            raise argparse.ArgumentTypeError(
                f"Number of problems cannot exceed 50, got {num}"
            )
        return num
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Number of problems must be a valid integer, got '{num_str}'"
        )


def validate_topic(topic_str: str) -> str:
    """
    Validate and normalize topic name.

    Args:
        topic_str: Topic name

    Returns:
        Normalized topic name

    Raises:
        argparse.ArgumentTypeError: If topic is invalid
    """
    if not topic_str or len(topic_str) < 2:
        raise argparse.ArgumentTypeError(
            "Topic must be at least 2 characters long"
        )
    if len(topic_str) > 100:
        raise argparse.ArgumentTypeError(
            "Topic must not exceed 100 characters"
        )
    return topic_str.strip()


# ==============================================================================
# CLI Functions
# ==============================================================================

def arguments_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="Fetch famous unsolved problems for a given topic",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python unsolved.py -t "Mathematics" -n 10
  python unsolved.py --topic "Physics" --num-problems 5
  python unsolved.py -t "Computer Science" -n 8 -m claude-3-opus
  DEFAULT_LLM_MODEL=gpt-4 python unsolved.py -t "Biology" -n 10
        """
    )

    parser.add_argument(
        "-t",
        required=True,
        type=validate_topic,
        dest="topic",
        help="Topic to find unsolved problems for (e.g., 'Mathematics', 'Physics', 'Chemistry')"
    )

    parser.add_argument(
        "-n",
        required=True,
        type=validate_num_problems,
        dest="num_problems",
        help="Number of unsolved problems to retrieve (1-50)"
    )

    parser.add_argument(
        "-m",
        default=None,
        dest="model",
        help="LLM model to use (default: $DEFAULT_LLM_MODEL or ollama/gemma3)"
    )

    return parser


def main() -> int:
    """
    Main entry point for the unsolved problems CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = arguments_parser()
    args = parser.parse_args()

    try:
        logger.info(f"Fetching {args.num_problems} unsolved problems in {args.topic}...")

        problems = fetch_unsolved_problems(args.topic, args.num_problems, model=args.model)

        if not problems:
            logger.error("No unsolved problems returned from API")
            return 1

        # Ensure outputs directory exists
        outputs_dir = Path(__file__).parent / "outputs"
        outputs_dir.mkdir(parents=True, exist_ok=True)

        # Generate automatic filename: unsolved_{topic}_{count}.json
        safe_topic = re.sub(r'[^a-zA-Z0-9_-]', '_', args.topic.lower())
        output_filename = outputs_dir / f"unsolved_{safe_topic}_{args.num_problems}.json"

        data_to_save = {
            "topic": args.topic,
            "num_problems": args.num_problems,
            "problems_retrieved": len(problems),
            "problems": [problem.model_dump() for problem in problems]
        }

        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)

        os.chmod(output_filename, 0o600)

        logger.info(f"Successfully saved {len(problems)} unsolved problem(s) to {output_filename}")
        print( "Generation complete ")
        return 0

    except RuntimeError as e:
        logger.error(f"Runtime error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except IOError as e:
        logger.error(f"File I/O error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
