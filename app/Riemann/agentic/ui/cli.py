#!/usr/bin/env python3
"""riemann_problems_cli.py - CLI interface for Riemann Theory Guide

Contains command-line interface functions for the Riemann Theory reference guide,
including argument parsing, validation, and main entry point.
"""

import sys
import argparse
import logging
import random
from pathlib import Path

from lite.config import ModelConfig
from lite import logging_config
try:
    from .riemann_problems import RiemannTheoryGuide
    from .riemann_problems_agent import run_riemann_agent
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from riemann_problems import RiemannTheoryGuide
    from riemann_problems_agent import run_riemann_agent

# Global logger for application
logger = logging.getLogger(__name__)

def argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure argument parser for Riemann theory guide.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="Riemann Theory Reference Guide - Dynamically fetches comprehensive documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python riemann_problems_cli.py                              # Show summary of all theories
  python riemann_problems_cli.py -t "Riemann Hypothesis"      # Show details of Riemann Hypothesis
  python riemann_problems_cli.py -t "Riemannian manifold"     # Show details of Riemannian manifold
  python riemann_problems_cli.py -e                           # Show an example of a Riemann theory
  python riemann_problems_cli.py -m ollama/gemma3             # Use specific model
        """
    )

    parser.add_argument(
        "-t", "--theory",
        type=str,
        help="Name of the Riemann theory or concept to display details. If not specified, shows summary."
    )

    parser.add_argument(
        "-e", "--example",
        action="store_true",
        help="Display an example of a Riemann theory (chooses one at random)."
    )

    parser.add_argument(
        "-m", "--model",
        default="ollama/gemma3",
        help="Model to use for fetching theory information (default: ollama/gemma3)"
    )

    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List all available Riemann theories from assets/riemann.txt"
    )

    return parser

import asyncio

# Global logger for application
logger = logging.getLogger(__name__)

async def run_agent_generation(theory_name: str, model: str):
    """Run the agentic generation process."""
    print(f"\n🔄 Running Agentic Researcher for: '{theory_name}'...")
    try:
        theory_data = await run_riemann_agent(theory_name, model=model)
        RiemannTheoryGuide.display_theory(theory_data)
    except Exception as e:
        print(f"\n❌ Agent Error: {str(e)}")
        logger.error(f"Agent generation failed: {str(e)}")

def main():
    parser = argument_parser()
    args = parser.parse_args()

    try:
        # Initialize guide for assets loading
        guide = RiemannTheoryGuide(config=ModelConfig(model=args.model, temperature=0.3))

        if args.list:
            print("\nAvailable Riemann Theories (from assets/riemann.txt):")
            for theory in guide.available_theories:
                print(f" - {theory}")
            print()
            return

        theory_to_fetch = args.theory
        if args.example and not theory_to_fetch:
            if guide.available_theories:
                theory_to_fetch = random.choice(guide.available_theories)
                print(f"\n💡 Selected random theory as example: '{theory_to_fetch}'")
            else:
                print("\n⚠️ No theories found in assets/riemann.txt.")
                return

        # Display specific theory or summary
        if theory_to_fetch:
            asyncio.run(run_agent_generation(theory_to_fetch, args.model))
        else:
            guide.display_summary()

    except KeyboardInterrupt:
        print("\n\n⚠️ Operation cancelled by user")
        sys.exit(0)

    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
