import argparse
import logging
import json
import sys
import os
import re
from typing import Optional
from pydantic import BaseModel, Field, ValidationError

# Add parent directory to path to import lite module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lite import LiteClient, ModelConfig
from lite.config import ModelInput

# Configure logging to file only
def setup_logging(log_file: str = "unsolved.log") -> logging.Logger:
    """
    Configure logging to write to file only.

    Args:
        log_file: Path to log file

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # File handler with restricted permissions
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)

    # Add handlers to logger
    logger.addHandler(file_handler)

    # Set restrictive file permissions (owner read/write only)
    try:
        os.chmod(log_file, 0o600)
    except OSError:
        pass  # File may not exist yet, permissions will be set on first write

    return logger

logger = setup_logging()

# ==============================================================================
# Pydantic Models
# ==============================================================================

class UnsolvedProblem(BaseModel):
    """Represents an unsolved problem in a given field."""
    title: str = Field(..., description="The name or title of the unsolved problem")
    description: str = Field(..., description="Brief description of the problem and why it's important")
    field: str = Field(..., description="The specific field or subfield the problem belongs to")
    difficulty: str = Field(..., description="Estimated difficulty level (Elementary, Moderate, or Advanced)")
    first_posed: Optional[str] = Field(None, description="When or by whom the problem was first posed, if known")
    prize_money: Optional[str] = Field(None, description="Any prize money associated with solving this problem, if applicable")
    significance: str = Field(..., description="Why solving this problem would be significant for the field")
    current_status: str = Field(..., description="The best known results or current status as of today")


class UnsolvedProblemsResponse(BaseModel):
    """Response containing a list of unsolved problems."""
    topic: str = Field(..., description="The topic for which unsolved problems are listed")
    count: int = Field(..., description="Number of unsolved problems in the list")
    problems: list[UnsolvedProblem]


# ==============================================================================
# Core Functions
# ==============================================================================

def create_prompt(topic: str, num_problems: int) -> str:
    """
    Create the prompt for fetching unsolved problems in a given topic.

    Args:
        topic: The topic to find unsolved problems for
        num_problems: Number of unsolved problems to retrieve

    Returns:
        Formatted prompt string for the LLM
    """
    return f"""Provide a list of {num_problems} famous unsolved problems in {topic}.

For each problem, provide:
1. Title: The name of the problem
2. Description: A brief, clear explanation of what the problem is and why it matters
3. Field: The specific field or subfield it belongs to
4. Difficulty: Estimated difficulty level (Elementary, Moderate, or Advanced)
5. First Posed: When or by whom the problem was first posed (if known)
6. Prize Money: Any prize money associated with solving it (if applicable)
7. Significance: Why solving this problem would be significant for the field
8. Current Status: The best known results or current status as of today (describe recent progress, partial solutions, or approaches)

Focus on well-known, legitimate unsolved problems in {topic}. Use objective language and avoid speculation.
Ensure the problems are academically recognized and well-documented."""


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
        model: LLM model to use (defaults to environment variable or gemini/gemini-2.5-flash)

    Returns:
        List of UnsolvedProblem instances

    Raises:
        ValueError: If API response is invalid or model response doesn't match schema
        RuntimeError: If API call fails or required credentials are missing
    """
    if model is None:
        model = os.getenv("UNSOLVED_MODEL", "gemini/gemini-2.5-flash")

    if not re.match(r'^[a-zA-Z0-9\-\./_]+$', model):
        raise ValueError(f"Invalid model name: {model}. Only alphanumeric characters, hyphens, slashes, dots, and underscores are allowed.")

    if num_problems < 1 or num_problems > 50:
        raise ValueError(f"Number of problems must be between 1 and 50, got {num_problems}")

    logger.info(f"Fetching {num_problems} unsolved problems in {topic} using model: {model}")

    try:
        # Create ModelConfig and LiteClient
        model_config = ModelConfig(model=model, temperature=0.2)
        client = LiteClient(model_config=model_config)

        # Create ModelInput with prompt and response format
        model_input = ModelInput(
            user_prompt=create_prompt(topic, num_problems),
            response_format=UnsolvedProblemsResponse
        )

        # Generate text using LiteClient
        response_content = client.generate_text(model_input=model_input)

        # Parse the response
        if isinstance(response_content, str):
            response = UnsolvedProblemsResponse.model_validate_json(response_content)
        else:
            raise ValueError("Expected string response from model")

        if not response.problems or len(response.problems) == 0:
            raise ValueError("No unsolved problems returned in response")

        logger.info(f"Successfully fetched {len(response.problems)} unsolved problem(s)")
        return response.problems

    except Exception as e:
        _handle_api_error(e)


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
  UNSOLVED_MODEL=gpt-4 python unsolved.py -t "Biology" -n 10
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
        help="LLM model to use (default: $UNSOLVED_MODEL or gemini/gemini-2.5-flash)"
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

        # Generate automatic filename: unsolved_{topic}_{count}.json
        safe_topic = re.sub(r'[^a-zA-Z0-9_-]', '_', args.topic.lower())
        output_filename = f"unsolved_{safe_topic}_{args.num_problems}.json"

        data_to_save = {
            "topic": args.topic,
            "num_problems": args.num_problems,
            "problems_retrieved": len(problems),
            "problems": [problem.model_dump() for problem in problems]
        }

        with open(output_filename, 'w') as f:
            json.dump(data_to_save, f, indent=4)

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
