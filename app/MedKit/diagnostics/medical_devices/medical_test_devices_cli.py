import argparse
import logging
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.config import ModelConfig
from lite.logging_config import configure_logging

from medical_test_devices import MedicalTestDeviceGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the medical test device generator CLI.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Generate comprehensive information for a medical device.")
    parser.add_argument("-i", "--input", type=str, required=True, help="The name of the medical device to generate information for.")
    parser.add_argument("-o", "--output", type=str, help="Optional: The specific path to save the output file.")
    parser.add_argument("--output-dir", type=str, default="outputs", help="The directory to save output files. Default: outputs.")
    parser.add_argument("-m", "--model", type=str, default="ollama/gemma3", help="Model to use for generation (default: ollama/gemma3).")
    parser.add_argument("-v", "--verbosity", type=int, default=2, help="Logging verbosity level (0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG). Default: 2.")
    parser.add_argument(
        "-s", "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response."
    )

    return parser.parse_args()


def create_medical_test_device_report(args):

    # Ensure logs directory exists
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    # Apply logging configuration at the entry point
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "medical_test_devices.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        generator = MedicalTestDeviceGenerator(model_config)

        # Generate the device information
        result = generator.generate_text(args.input, structured=args.structured)
        
        # Determine output path and ensure directory exists
        if args.output:
            output_path = Path(args.output)
            output_dir = output_path.parent
        else:
            output_dir = Path(args.output_dir)
            output_path = output_dir / f"{args.input.lower().replace(' ', '_')}.json"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save results
        saved_path = generator.save(result, output_path)
        
    except Exception as e:
        logger.error(f"Critical error during CLI execution: {e}", exc_info=True)

if __name__ == "__main__":
    args = get_user_arguments()
    create_medical_test_device_report(args)
