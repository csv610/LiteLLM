import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging
from medical_test_devices import MedicalTestDeviceGuide
from tqdm import tqdm

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the medical test device generator CLI.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate comprehensive information for a medical device."
    )
    parser.add_argument(
        "test_device",
        type=str,
        help="The name of the medical test device OR a file path containing device names (one per line).",
    )

    # These are common arguments..

    parser.add_argument(
        "-d",
        "--output-dir",
        type=str,
        default="outputs",
        help="The directory to save output files. Default: outputs.",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="ollama/gemma3",
        help="Model to use for generation (default: ollama/gemma3).",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        help="Logging verbosity level (0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG). Default: 2.",
    )
    parser.add_argument(
        "-s",
        "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response.",
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
        enable_console=True,
    )

    # Determine output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine devices to process
    test_device_input = args.test_device
    devices = []

    if Path(test_device_input).is_file():
        logger.info(f"Reading device list from file: {test_device_input}")
        with open(test_device_input, "r") as f:
            devices = [line.strip() for line in f if line.strip()]
    else:
        devices = [test_device_input]

    if not devices:
        logger.warning("No devices found to process.")
        return

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedicalTestDeviceGuide(model_config)

        # Process devices one by one with tqdm
        for device in tqdm(devices, desc="Generating reports", unit="device"):
            try:
                # Generate the device information (expensive operation)
                result = generator.generate_text(device, structured=args.structured)

                # Determine output file path
                safe_name = device.lower().replace(" ", "_").replace("/", "_")
                extension = ".json" if args.structured else ".md"
                output_file = output_dir / f"{safe_name}{extension}"

                # Save results
                saved_path = generator.save(result, output_file)
                logger.info(
                    f"✓ Medical test device information for '{device}' saved to: {saved_path}"
                )
            except Exception as e:
                logger.error(f"Error processing device '{device}': {e}")
                continue

    except Exception as e:
        logger.error(f"Critical error during CLI execution: {e}", exc_info=True)


def main():
    args = get_user_arguments()
    create_medical_test_device_report(args)


if __name__ == "__main__":
    main()
