#!/usr/bin/env python3
"""Command-line interface for LiteText - Query language models from various providers."""

import argparse
import logging
import sys

from src.litellm_tools import LiteText, ModelConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def format_output(result, model: str) -> None:
    """
    Format and print the response results.

    Args:
        result: LiteTextResponse object
        model: Model identifier that was used
    """
    print(f"\nModel: {model}")
    print("-" * 60)

    if result.is_success():
        print(f"Response: {result.response}\n")
        print(f"Response Time: {result.response_time:.2f} seconds")
        print(f"Word Count: {result.word_count}")
    else:
        print(f"Error: {result.error}")


def list_available_models() -> None:
    """Display all available models with their indices."""
    models = ModelConfig.get_models("text")
    print("Available models:")
    print("-" * 60)
    for i, model in enumerate(models):
        provider = model.split("/")[0].upper()
        print(f"{i:2d}: [{provider:6s}] {model}")
    print()


def cli_interface() -> None:
    """Parse command-line arguments and execute the LiteText query."""
    parser = argparse.ArgumentParser(
        description="CLI for LiteText API - Query language models from various providers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
        "  python cli_litetext.py -p 'What is AI?' -m 0\n"
        "  python cli_litetext.py --prompt 'Explain quantum computing' --model 5\n"
        "  python cli_litetext.py -p 'Hello' --list-models",
    )
    parser.add_argument(
        "-p",
        "--prompt",
        type=str,
        help="Input prompt for the model",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=int,
        default=0,
        help="Index of the model to use (default: 0)",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List all available models and exit",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=LiteText.DEFAULT_TEMPERATURE,
        help="Sampling temperature (default: 0.2)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=LiteText.DEFAULT_MAX_TOKENS,
        help="Maximum tokens in response (default: 1000)",
    )

    args = parser.parse_args()

    if args.list_models:
        list_available_models()
        return

    if not args.prompt:
        parser.error("The following arguments are required: -p/--prompt")

    model = ModelConfig.get_model(args.model, "text")
    if model is None:
        print(f"Error: Invalid model index {args.model}")
        list_available_models()
        sys.exit(1)

    result = LiteText.get_response(
        args.prompt,
        model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )
    format_output(result, model)

    if not result.is_success():
        sys.exit(1)


if __name__ == "__main__":
    cli_interface()
