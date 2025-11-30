#!/usr/bin/env python3
"""Unified CLI for LiteClient - Query language models and analyze images."""

import argparse
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lite.lite_client import LiteClient
from lite.config import ModelConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def list_available_models(model_type: str = "text") -> None:
    """Display all available models with their indices."""
    models = ModelConfig.get_models(model_type)
    mode = "text" if model_type == "text" else "vision"
    print(f"\nAvailable {mode} models:")
    print("-" * 60)
    for i, model in enumerate(models):
        provider = model.split("/")[0].upper()
        print(f"{i:2d}: [{provider:6s}] {model}")
    print()


def cli_interface() -> None:
    """Parse command-line arguments and execute the unified LiteClient."""
    parser = argparse.ArgumentParser(
        description="Unified CLI for LiteClient - Text generation and image analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
        "  # Text query\n"
        "  python liteclient_cli.py -q 'What is AI?'\n"
        "  python liteclient_cli.py -q 'Explain quantum computing' -m 5 -t 0.7\n"
        "\n"
        "  # Image analysis\n"
        "  python liteclient_cli.py -i photo.jpg\n"
        "  python liteclient_cli.py -i diagram.png -q 'What is shown here?' -m 3\n"
        "\n"
        "  # List models\n"
        "  python liteclient_cli.py --list-models\n"
        "  python liteclient_cli.py --list-models vision",
    )
    parser.add_argument(
        "-q",
        "--question",
        type=str,
        help="Input prompt for the model or image analysis",
    )
    parser.add_argument(
        "-i",
        "--image",
        type=str,
        default=None,
        help="Path to the image file (PNG, JPG, PDF) for vision analysis",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=int,
        default=0,
        help="Index of the model to use (default: 0)",
    )
    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        default=LiteClient.DEFAULT_TEMPERATURE,
        help=f"Sampling temperature (default: {LiteClient.DEFAULT_TEMPERATURE})",
    )
    parser.add_argument(
        "--list-models",
        nargs="?",
        const="text",
        choices=["text", "vision"],
        help="List available models (text or vision, default: text)",
    )

    args = parser.parse_args()

    # Handle list-models flag
    if args.list_models is not None:
        list_available_models(args.list_models)
        return

    # Determine mode based on image argument
    if args.image:
        model_type = "vision"
        if not args.question:
            args.question = "Describe the image"
    else:
        model_type = "text"
        if not args.question:
            parser.error("The following arguments are required: -q/--question")

    # Get model
    model = ModelConfig.get_model(args.model, model_type)
    if model is None:
        print(f"Error: Invalid model index {args.model}")
        list_available_models(model_type)
        sys.exit(1)

    # Execute request
    client = LiteClient()
    result = client.generate_text(
        prompt=args.question,
        image_path=args.image,
        model=model,
        temperature=args.temperature,
    )

    # Display result
    print(f"\nModel: {model}")
    print("-" * 60)

    if isinstance(result, dict) and "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)
    else:
        print(f"Response: {result}\n")


if __name__ == "__main__":
    cli_interface()
