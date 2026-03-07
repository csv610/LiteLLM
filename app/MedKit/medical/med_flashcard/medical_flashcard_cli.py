"""Medical Flashcard Generator CLI (from Images)."""

import sys
from pathlib import Path

# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging
from tqdm import tqdm

try:
    from .medical_flashcard import MedicalLabelExtractor, MedicalTermExplainer
except (ImportError, ValueError):
    from medical.med_flashcard.medical_flashcard import (
        MedicalLabelExtractor,
        MedicalTermExplainer,
    )

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Explain medical labels extracted from images."
    )
    parser.add_argument("image", help="Path to image or file containing image paths.")
    parser.add_argument(
        "-d", "--output-dir", default="outputs", help="Output directory."
    )
    parser.add_argument(
        "-m",
        "--model",
        default="ollama/gemma3",
        help="Model for extraction/explanation.",
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
    return parser.parse_args()


def main():
    args = get_user_arguments()
    configure_logging(
        log_file="medical_flashcard.log", verbosity=args.verbosity, enable_console=True
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.image)
    images = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        and input_path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]
        else [args.image]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.5)
        extractor = MedicalLabelExtractor(model_config)
        explainer = MedicalTermExplainer(model_config)

        for img in tqdm(images, desc="Processing Images"):
            logger.info(f"Processing: {img}")
            terms = extractor.extract_terms(img)
            if not terms:
                logger.warning(f"No terms found in {img}")
                continue

            results = explainer.explain_terms(terms, structured=args.structured)
            for term, info in results:
                explainer.save(info, output_dir, term=term)

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
