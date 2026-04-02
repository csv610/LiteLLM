#!/usr/bin/env python3
"""studyguide_cli.py - CLI interface for book summary generation

Contains command-line interface for generating detailed book summaries.
"""

import sys
import argparse
from pathlib import Path

# Add project root directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from lite.config import ModelConfig
from lite import logging_config
from .studyguide_models import BookInput
from .studyguide_generator import StudyGuideGenerator

# Global logger for application
logger = None


def cli(title, author=None, model_name="ollama/gemma3"):
    """Generate a detailed summary for a book using StudyGuideGenerator.

    Args:
        title (str): The title of the book
        author (str): The author of the book (optional)
        model_name (str): The model to use for generation
    """
    global logger
    
    try:
        # Initialize global logger
        logger = logging_config.configure_logging(str(Path(__file__).parent.parent / "logs" / "studyguide.log"))
        
        # Create ModelConfig and StudyGuideGenerator
        model_config = ModelConfig(model=model_name, temperature=0.2)
        generator = StudyGuideGenerator(model_config)

        # Create BookInput
        book_input = BookInput(
            title=title,
            author=author
        )

        # Generate and save summary
        output_file = generator.generate_and_save(book_input)

        author_display = f" by {author}" if author else ""
        print(f"Detailed summary for '{title}'{author_display} saved to {output_file}")

    except Exception as e:
        if logger:
            logger.error(f"Error: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a detailed summary for any book.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate summary for a book by title
  python studyguide_cli.py 'The Great Gatsby'

  # Generate summary with title and author
  python studyguide_cli.py 'Thinking, Fast and Slow' -a 'Daniel Kahneman'

  # Use a custom model
  python studyguide_cli.py '1984' -m 'openai/gpt-4o'
        """
    )

    parser.add_argument(
        "title",
        help="Title of the book to summarize"
    )
    parser.add_argument(
        "-a", "--author",
        default=None,
        help="Author of the book"
    )
    parser.add_argument(
        "-m", "--model",
        default="ollama/gemma3",
        help="LLM model to use (default: ollama/gemma3)"
    )

    args = parser.parse_args()
    cli(args.title, args.author, args.model)
