import argparse
import logging

from pathlib import Path

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
    parser.add_argument("-i", "--test-device", "--test_device", type=str, required=True, help="The name of the medical test device to generate information for.")
    parser.add_argument("-d", "--output-dir", type=str, default="outputs", help="The directory to save output files. Default: outputs.")
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

    # Determine output directory and base filename FIRST (fail-fast validation)
    output_dir = Path(args.output_dir)
    base_filename = f"{args.test_device.lower().replace(' ', '_')}"
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedicalTestDeviceGenerator(model_config)

        # Generate the device information (expensive operation)
        result = generator.generate_text(args.test_device, structured=args.structured)
        
        # Save results
        saved_path = generator.save(result, output_dir / base_filename)
        
    except Exception as e:
        logger.error(f"Critical error during CLI execution: {e}", exc_info=True)

if __name__ == "__main__":
    args = get_user_arguments()
    create_medical_test_device_report(args)
