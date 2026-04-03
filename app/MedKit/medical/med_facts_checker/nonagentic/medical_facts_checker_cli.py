"""Medical Facts Checker CLI."""

import sys
from pathlib import Path

# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


import argparse
import logging

from lite.config import ModelConfig
from lite.logging_config import configure_logging
from lite.utils import save_model_response
from tqdm import tqdm

try:
    from .medical_facts_checker import MedicalFactsChecker
except (ImportError, ValueError):
    from medical.med_facts_checker.nonagentic.medical_facts_checker import (
        MedicalFactsChecker,
    )

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze statements and determine if they are fact or fiction."
    )
    parser.add_argument(
        "statement", help="Statement or file path containing statements."
    )
    parser.add_argument(
        "-d", "--output-dir", default="outputs", help="Output directory."
    )
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
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
        log_file="medical_facts_checker.log",
        verbosity=args.verbosity,
        enable_console=True,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.statement)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.statement]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        checker = MedicalFactsChecker(model_config)

        for item in tqdm(items, desc="Checking"):
            result = checker.generate_text(statement=item, structured=args.structured)
            if result:
                fname = "".join([c if c.isalnum() else "_" for c in item.lower()])[:50]
                save_model_response(result, output_dir / f"{fname}.json")

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
