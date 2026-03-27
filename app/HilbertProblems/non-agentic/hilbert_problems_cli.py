#!/usr/bin/env python3
"""hilbert_problems_cli.py - CLI interface for Hilbert's 23 Problems

Contains command-line interface functions for the Hilbert Problems reference guide,
including argument parsing, validation, and main entry point.
"""

import sys
import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite import logging_config
from hilbert_problems import HilbertProblemsGuide

# Global logger for application
logger = logging.getLogger(__name__)

def argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure argument parser for Hilbert problems guide.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="Hilbert's 23 Problems Reference Guide - Dynamically fetches comprehensive documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python hilbert_problems_cli.py                              # Show all problems summary
  python hilbert_problems_cli.py -p 1                         # Show details of problem 1
  python hilbert_problems_cli.py -p 8 -m ollama/gemma3       # Show problem 8 using specific model
  python hilbert_problems_cli.py -m ollama/mistral           # Show all problems with custom model
        """
    )

    parser.add_argument(
        "-p", "--problem",
        type=int,
        help="Problem number (1-23) to display details. If not specified, shows summary of all problems"
    )

    parser.add_argument(
        "-m", "--model",
        default="ollama/gemma3",
        help="Model to use for fetching problem information (default: ollama/gemma3)"
    )

    return parser


def main():
    parser = argument_parser()
    args = parser.parse_args()

    try:
        # Initialize global logger
        logging_config.configure_logging(str(Path(__file__).parent / "logs" / "hilbert_problems_cli.log"))
        
        # Initialize guide with specified model
        model_config = ModelConfig(model=args.model, temperature=0.3)
        guide = HilbertProblemsGuide(model_config)

        # Display specific problem or summary
        if args.problem:
            if args.problem < 1 or args.problem > 23:
                print(f"\n❌ Invalid problem number: {args.problem}")
                print("Please specify a number between 1 and 23\n")
                return

            print(f"\n🔄 Fetching Problem {args.problem}...")
            problem = guide.generate_text(args.problem)
            HilbertProblemsGuide.display_problem(problem)
        else:
            guide.display_summary()

    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(0)

    except Exception as e:
        if logger:
            logger.error(f"Unexpected error: {str(e)}")
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
