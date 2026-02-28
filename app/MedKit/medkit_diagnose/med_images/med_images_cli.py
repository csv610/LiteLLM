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
    parser = argparse.ArgumentParser(description="Classify medical images.")
    parser.add_argument("input", type=str, help="Image file path or directory of images.")

    parser.add_argument("-d", "--output-dir", default="outputs", help="Directory for output files (default: outputs).")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use (default: ollama/gemma3).")
    parser.add_argument("-v", "--verbosity", type=int, default=3, choices=[0, 1, 2, 3, 4], help="Logging verbosity (default: 3).")
    parser.add_argument("-s", "--structured", action="store_true", default=True, help="Use structured output (default: True).")

    return parser.parse_args()


def create_med_images_report(args) -> int:
    """Classify medical images."""
    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "med_images.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    input_path = Path(args.input)
    supported_image_ext = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}
    
    items_to_process = []

    # Determine what to process
    if input_path.is_file():
        if input_path.suffix.lower() in supported_image_ext:
            items_to_process = [str(input_path)]
        else:
            logger.info(f"Reading image list from file: {args.input}")
            with open(input_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and Path(line).suffix.lower() in supported_image_ext:
                        items_to_process.append(line)
    elif input_path.is_dir():
        logger.info(f"Processing all images in directory: {args.input}")
        for img_file in input_path.iterdir():
            if img_file.suffix.lower() in supported_image_ext:
                items_to_process.append(str(img_file))
    elif input_path.suffix.lower() in supported_image_ext:
        items_to_process = [args.input]

    if not items_to_process:
        logger.error("No valid image files provided to process.")
        return 1

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    exit_code = 0
    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedImageClassifier(model_config)
        
        # Use tqdm for a progress bar
        pbar = tqdm(items_to_process, desc="Classifying", unit="image", disable=len(items_to_process) <= 1)
        for item in pbar:
            pbar.set_description(f"Classifying: {Path(item).name}")
            logger.info(f"Classifying medical image: {item}")
            
            try:
                result = generator.classify_image(item, structured=args.structured)
                if result is None:
                    logger.error(f"✗ Failed to classify: {item}")
                    exit_code = 1
                    continue

                # Save result to output directory
                saved_path = generator.save(result, output_dir)
                logger.info(f"✓ Results saved to: {saved_path}")
            except Exception as e:
                logger.error(f"✗ Error processing {item}: {e}")
                exit_code = 1
            
        return exit_code
    except Exception as e:
        logger.error(f"✗ Process failed: {e}")
        return 1



def main():
    args = get_user_arguments()
    create_med_images_report(args)

if __name__ == "__main__":
   main()
