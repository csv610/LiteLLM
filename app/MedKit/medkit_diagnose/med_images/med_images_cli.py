"""med_images_cli.py - Generate comprehensive med image classification information."""

import argparse
import logging
from pathlib import Path

from tqdm import tqdm
from lite.config import ModelConfig
from lite.logging_config import configure_logging

from med_images import MedImageClassifier

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Generate med image classification information or classify medical images.")
    parser.add_argument("input", type=str, help="med image classification name, image file path, or path to a file containing a list (one per line).")

    parser.add_argument("-d", "--output-dir", default="outputs", help="Directory for output files (default: outputs).")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use for generation (default: ollama/gemma3).")
    parser.add_argument("-v", "--verbosity", type=int, default=3, choices=[0, 1, 2, 3, 4], help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 3).")
    parser.add_argument("-s", "--structured", action="store_true", default=False, help="Use structured output (Pydantic model) for the response.")
    parser.add_argument("-i", "--image", action="store_true", default=False, help="Force image classification mode for the input path.")

    return parser.parse_args()


def create_med_images_report(args) -> int:
    """Generate med image classification information or classify images."""
    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "med_images.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    input_path = Path(args.input)
    supported_image_ext = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}
    
    items_to_process = []
    is_image_mode = args.image

    # Determine what to process
    if input_path.is_file():
        if input_path.suffix.lower() in supported_image_ext:
            items_to_process = [(str(input_path), True)]
        else:
            logger.info(f"Reading input list from file: {args.input}")
            with open(input_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    # Check if line looks like an image path
                    item_path = Path(line)
                    if item_path.suffix.lower() in supported_image_ext or is_image_mode:
                        items_to_process.append((line, True))
                    else:
                        items_to_process.append((line, False))
    elif input_path.suffix.lower() in supported_image_ext:
        # Path doesn't exist yet but looks like an image extension
        items_to_process = [(args.input, True)]
    else:
        # Assume it's a test name or a directory of images
        if is_image_mode and input_path.is_dir():
             logger.info(f"Processing all images in directory: {args.input}")
             for img_file in input_path.iterdir():
                 if img_file.suffix.lower() in supported_image_ext:
                     items_to_process.append((str(img_file), True))
        else:
            items_to_process = [(args.input, is_image_mode)]

    if not items_to_process:
        logger.error("No valid inputs provided to process.")
        return 1

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    exit_code = 0
    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedImageClassifier(model_config)
        
        # Use tqdm for a progress bar
        pbar = tqdm(items_to_process, desc="Processing", unit="item", disable=len(items_to_process) <= 1)
        for item, is_image in pbar:
            if is_image:
                pbar.set_description(f"Classifying Image: {Path(item).name}")
                logger.info(f"Classifying medical image: {item}")
                result = generator.classify_image(item, structured=args.structured)
            else:
                pbar.set_description(f"Processing Test: {item}")
                logger.info(f"Generating med image classification information for: {item}")
                result = generator.generate_text(item, structured=args.structured)

            if result is None:
                logger.error(f"✗ Failed to process: {item}")
                exit_code = 1
                continue

            # Save result to output directory
            saved_path = generator.save(result, output_dir)
            logger.info(f"✓ Results saved to: {saved_path}")
            
        return exit_code
    except Exception as e:
        logger.error(f"✗ Process failed: {e}")
        logger.exception("Full exception details:")
        return 1



def main():
    args = get_user_arguments()
    create_med_images_report(args)

if __name__ == "__main__":
   main()
