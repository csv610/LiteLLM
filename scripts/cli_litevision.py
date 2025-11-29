#!/usr/bin/env python3
"""Command-line interface for LiteVision - Analyze images using AI models."""

import argparse
import logging
import sys

from lite.litellm_tools import LiteVision, ModelConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def cli_app() -> None:
    """Parse command-line arguments and analyze an image."""
    models = ModelConfig.get_models("vision")

    parser = argparse.ArgumentParser(
        description="Analyze an image using AI models from various providers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
        "  python cli_litevision.py -i photo.jpg -p 'Describe the image'\n"
        "  python cli_litevision.py -i diagram.png -p 'What is shown?' -m 3\n"
        "  python cli_litevision.py -i image.jpg --list-models",
    )
    parser.add_argument(
        "-i",
        "--image",
        required=True,
        help="Path to the image file (PNG, JPG, PDF)",
    )
    parser.add_argument(
        "-p",
        "--prompt",
        default="Describe the image",
        help="Prompt to analyze the image (default: 'Describe the image')",
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
        help="List all available vision models and exit",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=LiteVision.DEFAULT_TEMPERATURE,
        help="Sampling temperature (default: 0.2)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=LiteVision.DEFAULT_MAX_TOKENS,
        help="Maximum tokens in response (default: 1000)",
    )

    args = parser.parse_args()

    if args.list_models:
        print("Available vision models:")
        print("-" * 60)
        for i, model in enumerate(models):
            provider = model.split("/")[0].upper()
            print(f"{i:2d}: [{provider:6s}] {model}")
        print()
        return

    model = ModelConfig.get_model(args.model, "vision")
    if model is None:
        print(f"Error: Invalid model index {args.model}")
        print(f"Please choose an index between 0 and {len(models) - 1}")
        sys.exit(1)

    result = LiteVision.get_response(
        args.prompt,
        args.image,
        model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )

    print(f"\nModel: {model}")
    print("-" * 60)

    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)
    else:
        print(f"Response: {result.get('text', 'N/A')}\n")
        print(f"Response Time: {result.get('response_time', 0):.2f} seconds")
        print(f"Word Count: {result.get('word_count', 0)}")


if __name__ == "__main__":
    cli_app()
