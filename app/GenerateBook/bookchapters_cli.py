#!/usr/bin/env python3
"""bookchapters_cli.py - CLI interface for book chapters generation

Contains command-line interface for educational curriculum generation,
including argument parsing and main entry point.
"""

import sys
import argparse
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lite.config import ModelConfig
from lite import logging_config
from bookchapters_models import BookInput
from bookchapters_generator import BookChaptersGenerator

# Global logger for application
logger = None


def cli(subject, level=None, num_chapters=12, model_name="ollama/gemma3"):
    """Generate chapter suggestions for a subject at a specific education level using BookChaptersGenerator.

    Args:
        subject (str): The subject or topic to create curriculum for
        level (str): The education level. If None, generates for all levels.
        num_chapters (int): Number of chapters to generate
        model_name (str): The model to use for generation
    """
    global logger
    
    try:
        # Initialize global logger
        logger = logging_config.setup_logging(str(Path(__file__).parent / "logs" / "bookchapters.log"))
        
        # Create ModelConfig and BookChaptersGenerator
        model_config = ModelConfig(model=model_name, temperature=0.2)
        generator = BookChaptersGenerator(model_config)

        # Create BookInput
        book_input = BookInput(
            subject=subject,
            level=level,
            num_chapters=num_chapters
        )

        # Generate and save curriculum
        output_file = generator.generate_and_save(book_input)

        level_display = level if level else 'All Levels'
        print(f"Chapter suggestions for '{subject}' ({level_display}) saved to {output_file}")

    except Exception as e:
        if logger:
            logger.error(f"Error: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    from bookchapters_prompts import EDUCATION_LEVELS, LEVEL_CODES
    
    levels_help = '\n'.join(f"  {code}: {level}" for level, code in LEVEL_CODES.items())

    parser = argparse.ArgumentParser(
        description="Generate educational curriculum chapters for any subject across education levels.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Education Levels:
{levels_help}

Examples:
  # Generate for all 6 levels (default)
  python bookchapters_cli.py 'Quantum Physics'

  # Generate for specific level
  python bookchapters_cli.py 'Climate Change' -l 'High School'
  python bookchapters_cli.py 'Machine Learning' -l Undergraduate -n 5

  # Use custom model
  python bookchapters_cli.py 'AI' -l 'Post-Graduate' -m 'openai/gpt-4'
  python bookchapters_cli.py 'Black Holes' -l 'General Public' -n 8 -m 'anthropic/claude-3-5-sonnet'
        """
    )

    parser.add_argument(
        "subject",
        help="Subject or topic to create curriculum for"
    )
    parser.add_argument(
        "-l", "--level",
        default=None,
        help="Education level. Omit to generate for all 6 levels"
    )
    parser.add_argument(
        "-n", "--chapters",
        type=int,
        default=12,
        help="Number of chapters per level (default: 12)"
    )
    parser.add_argument(
        "-m", "--model",
        default="ollama/gemma3",
        help="LLM model to use (default: ollama/gemma3)"
    )

    args = parser.parse_args()
    cli(args.subject, args.level, args.chapters, args.model)
