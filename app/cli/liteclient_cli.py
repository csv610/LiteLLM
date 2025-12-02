#!/usr/bin/env python3
"""Unified CLI for LiteClient - Query language models and analyze images."""

import argparse
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput, DEFAULT_TEMPERATURE

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)



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
        type=str,
        default="gemini/gemini-2.5-flash",
        help="Model name to use (default: gemini/gemini-2.5-flash)",
    )
    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help=f"Sampling temperature (default: {DEFAULT_TEMPERATURE})",
    )
    args = parser.parse_args()

    # Determine mode based on image argument
    if args.image:
        model_type = "vision"
        if not args.question:
            args.question = "Describe the image"
    else:
        model_type = "text"
        if not args.question:
            parser.error("The following arguments are required: -q/--question")

    # Execute request
    model_config = ModelConfig(model=args.model, temperature=args.temperature)
    client = LiteClient(model_config=model_config)
    model_input = ModelInput(user_prompt=args.question, image_path=args.image)
    result = client.generate_text(model_input=model_input)

    # Display result
    print(f"\nModel: {args.model}")
    print("-" * 60)

    if isinstance(result, dict) and "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)
    else:
        print(f"Response: {result}\n")


if __name__ == "__main__":
    cli_interface()
