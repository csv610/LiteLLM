import argparse
import logging
import sys
from pathlib import Path

from tqdm import tqdm

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from lite.config import ModelConfig
from lite.logging_config import configure_logging

# Import generators from diagnostics package
try:
    from medkit_diagnose.med_devices.medical_test_devices import MedicalTestDeviceGuide
    from medkit_diagnose.med_images.med_images import MedImageClassifier
    from medkit_diagnose.med_tests.medical_test_info import MedicalTestInfoGenerator
except (ImportError, ValueError):
    try:
        from .med_devices.medical_test_devices import MedicalTestDeviceGuide
        from .med_images.med_images import MedImageClassifier
        from .med_tests.medical_test_info import MedicalTestInfoGenerator
    except (ImportError, ValueError):
        from med_devices.medical_test_devices import MedicalTestDeviceGuide
        from med_images.med_images import MedImageClassifier
        from med_tests.medical_test_info import MedicalTestInfoGenerator

logger = logging.getLogger(__name__)


def handle_batch_input(input_val: str, desc: str):
    input_path = Path(input_val)
    if input_path.is_file():
        # Check if it's an image file first for classify_image command
        supported_image_ext = {
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".webp",
            ".bmp",
            ".tiff",
        }
        if input_path.suffix.lower() in supported_image_ext:
            return [input_val]

        with open(input_path, "r", encoding="utf-8") as f:
            items = [line.strip() for line in f if line.strip()]
        logger.debug(f"Read {len(items)} items from file: {input_path}")
        return items
    elif input_path.is_dir():
        supported_image_ext = {
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".webp",
            ".bmp",
            ".tiff",
        }
        items = [
            str(p)
            for p in input_path.iterdir()
            if p.suffix.lower() in supported_image_ext
        ]
        logger.debug(f"Found {len(items)} images in directory: {input_path}")
        return items
    return [input_val]


def main():
    parser = argparse.ArgumentParser(
        description="MedKit Diagnose CLI - Medical tests, devices and image classification."
    )

    # Global arguments
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument(
        "-d", "--output-dir", default="outputs", help="Output directory."
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Verbosity level.",
    )
    parser.add_argument(
        "-s", "--structured", action="store_true", help="Use structured output."
    )

    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Diagnose subcommands"
    )

    # 1. Medical Tests
    test_p = subparsers.add_parser(
        "test", help="Get information about medical laboratory tests"
    )
    test_p.add_argument(
        "test", help="Test name (e.g., 'HbA1c', 'Complete Blood Count')"
    )

    # 2. Medical Devices
    device_p = subparsers.add_parser(
        "device", help="Get information about medical diagnostic devices"
    )
    device_p.add_argument(
        "device", help="Device name (e.g., 'MRI Scanner', 'Insulin Pump')"
    )

    # 3. Medical Image Classification
    image_p = subparsers.add_parser(
        "classify_image", help="Classify medical diagnostic images"
    )
    image_p.add_argument("image", help="Path to image file or directory")

    args = parser.parse_args()

    # Logging config
    configure_logging(
        log_file="medkit_diagnose.log", verbosity=args.verbosity, enable_console=True
    )
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model_config = ModelConfig(model=args.model, temperature=0.2)

    try:
        if args.command == "test":
            gen = MedicalTestInfoGenerator(model_config)
            for item in tqdm(handle_batch_input(args.test, "test"), desc="Tests"):
                res = gen.generate_text(test_name=item, structured=args.structured)
                if res:
                    gen.save(res, output_dir)

        elif args.command == "device":
            gen = MedicalTestDeviceGuide(model_config)
            for item in tqdm(handle_batch_input(args.device, "device"), desc="Devices"):
                res = gen.generate_text(device_name=item, structured=args.structured)
                if res:
                    gen.save(res, output_dir)

        elif args.command == "classify_image":
            gen = MedImageClassifier(model_config)
            items = handle_batch_input(args.image, "image")
            for item in tqdm(items, desc="Classifying Images"):
                res = gen.classify_image(item, structured=args.structured)
                if res:
                    gen.save(res, output_dir)

    except Exception as e:
        logger.error(f"Error in diagnostics command {args.command}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
