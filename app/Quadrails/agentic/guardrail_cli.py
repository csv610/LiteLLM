#!/usr/bin/env python3
"""guardrail_cli.py - CLI interface for text and image guardrailing.

Contains command-line interface functions for text and image guardrailing.
"""

import sys
import asyncio
import argparse
import logging
import os
from pathlib import Path

from lite.config import ModelConfig
from lite import logging_config
from .guardrail import GuardrailAnalyzer, TextGuardrailAgent, ImageGuardrailAgent, configure_module_logging
from .guardrail_models import GuardrailError

# Global logger for application
logger = logging.getLogger(__name__)

def argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure argument parser for guardrail.
    """
    default_model = os.getenv("GUARDRAIL_MODEL", "ollama/gemma3")
    
    parser = argparse.ArgumentParser(
        description="Quadrails CLI - Analyzes input text or image for safety violations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  python guardrail_cli.py -t "I hate you"                     # Analyze text
  python guardrail_cli.py -i ./sample.jpg                     # Analyze image for NSFW
  python guardrail_cli.py -t "Check this" -m {default_model}  # Specify model
        """
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-t", "--text",
        type=str,
        help="Input text to analyze for safety violations"
    )
    group.add_argument(
        "-i", "--image",
        type=str,
        help="Path to the image to analyze (NSFW check)"
    )

    parser.add_argument(
        "-m", "--model",
        default=default_model,
        help=f"Model to use for guardrail analysis (default: {default_model})"
    )

    parser.add_argument(
        "--max-length",
        type=int,
        default=4000,
        help="Maximum text length allowed (default: 4000)"
    )

    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable results caching"
    )

    return parser


async def run_analysis(args: argparse.Namespace):
    """Execution wrapper for async guardrail analyzer."""
    try:
        # Initialize global logger
        logging_config.configure_logging(str(Path(__file__).parent / "logs" / "guardrail_cli.log"))
        configure_module_logging()
        
        # Initialize agents with specified model
        model_config = ModelConfig(model=args.model, temperature=0.1)
        text_agent = TextGuardrailAgent(model_config, max_length=args.max_length)
        image_agent = ImageGuardrailAgent(model_config, max_length=args.max_length)

        # Run analysis
        if args.text:
            print("\n🔄 Analyzing text (Async)...")
            result = await text_agent.analyze_text(args.text, use_cache=not args.no_cache)
        elif args.image:
            print(f"\n🔄 Analyzing image (Async): {args.image}...")
            result = await image_agent.analyze_image(args.image, use_cache=not args.no_cache)
        else:
            print("\n❌ Error: Please provide either text (-t) or image (-i) input.")
            return
            
        # Display results
        GuardrailAnalyzer.display_results(result)

    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(0)

    except GuardrailError as e:
        logger.error(f"Guardrail specific error: {str(e)}")
        print(f"\n❌ Guardrail Error: {str(e)}")
        sys.exit(1)

    except Exception as e:
        if logger:
            logger.error(f"Unexpected system error: {str(e)}")
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)


def main():
    parser = argument_parser()
    args = parser.parse_args()

    if not args.text and not args.image:
        parser.print_help()
        sys.exit(0)

    # Launch the async event loop
    asyncio.run(run_analysis(args))


if __name__ == "__main__":
    main()
