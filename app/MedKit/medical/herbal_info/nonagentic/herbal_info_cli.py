"""Herbal Information Generator CLI."""

import argparse
import logging
import sys
from pathlib import Path

from tqdm import tqdm

# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from lite.config import ModelConfig
from lite.logging_config import configure_logging

try:
    from .herbal_info import HerbalInfoGenerator
except (ImportError, ValueError):
    from medical.herbal_info.nonagentic.herbal_info import HerbalInfoGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate comprehensive herbal information."
    )
    parser.add_argument("herb", help="Herb name or file path containing names.")
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
        log_file="herbal_info.log", verbosity=args.verbosity, enable_console=True
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.herb)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.herb]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = HerbalInfoGenerator(model_config)

        for item in tqdm(items, desc="Generating"):
            result = generator.generate_text(herb=item, structured=args.structured)
            if result:
                generator.save(result, output_dir)

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
