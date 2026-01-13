import argparse
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput, DEFAULT_TEMPERATURE
from logging_util import setup_logging

# Configure logging
logger = setup_logging(str(Path(__file__).parent / "logs" / "liteclient_cli.log"))


def main_cli() -> None:
    """Parse command-line arguments and execute the unified LiteClient."""
    parser = argparse.ArgumentParser(
        description="Unified CLI for LiteClient - Text generation and image analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
        "  # Text query\n"
        "  python liteclient_cli.py -q 'What is AI?'\n"
        "  python liteclient_cli.py -q 'Explain quantum computing' -t 0.7\n"
        "  python liteclient_cli.py -q 'What is AI?' -m gpt-4\n"
        "\n"
        "  # Image analysis (local file)\n"
        "  python liteclient_cli.py -i photo.jpg\n"
        "  python liteclient_cli.py -i diagram.png -q 'What is shown here?'\n"
        "\n"
        "  # Image analysis (URL)\n"
        "  python liteclient_cli.py -i https://example.com/image.jpg -q 'What is this?'\n"
    )
    parser.add_argument(
        "-q",
        "--question",
        type=str,
        help="Text prompt or question for the model. Required for text mode. "
             "Optional for image mode (defaults to 'Describe the image')",
    )
    parser.add_argument(
        "-i",
        "--image",
        type=str,
        default=None,
        help="Path to image file (PNG, JPG, PDF) or HTTP(S) URL for vision analysis. "
             "When provided, enables vision mode; when omitted, uses text mode",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="ollama/gemma3",
        help="Model identifier to use for generation (e.g., 'ollama/gemma3', 'gpt-4', etc.). "
             "Default: ollama/gemma3",
    )
    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help=f"Sampling temperature controlling output randomness (0.0=deterministic, 1.0=more random). "
             f"Default: {DEFAULT_TEMPERATURE}",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Optional path to output file for saving the response. "
             "If not specified, response is printed to stdout",
    )
    args = parser.parse_args()

    # Validate temperature range
    if not (0.0 <= args.temperature <= 2.0):
        parser.error(f"Temperature must be between 0.0 and 2.0, got {args.temperature}")

    # Determine mode based on image argument
    if args.image:
        if not args.question:
            args.question = "Describe the image"
    else:
        if not args.question:
            parser.error("The following arguments are required: -q/--question")

    # Execute request
    model_config = ModelConfig(model=args.model, temperature=args.temperature)
    client = LiteClient(model_config=model_config)
    model_input = ModelInput(user_prompt=args.question, image_path=args.image)
    result = client.generate_text(model_input=model_input)

    if isinstance(result, dict) and "error" in result:
        error_msg = f"Error: {result['error']}"
        logger.error(error_msg)
        if not args.output:
            print(f"\nModel: {args.model}")
            print("-" * 60)
            print(error_msg)
        sys.exit(1)
    else:
        # Save to output file if specified
        if args.output:
            try:
                with open(args.output, "w") as f:
                    f.write(result)
                logger.info(f"Response saved to {args.output}")
            except IOError as e:
                logger.error(f"Failed to write output file: {e}")
                print(f"Error: Could not write to file '{args.output}': {e}", file=sys.stderr)
                sys.exit(1)
        else:
            # Display result only if no output file
            print(f"\nModel: {args.model}")
            print("-" * 60)
            print(f"Response: {result}\n")
            logger.info("Response generated successfully")

if __name__ == "__main__":
    main_cli()
