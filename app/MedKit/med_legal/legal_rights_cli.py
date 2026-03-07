"""Patient Legal Rights Information Generator CLI."""

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

try:
    from med_legal.legal_rights import LegalRightsGenerator
except (ImportError, ValueError):
    from legal_rights import LegalRightsGenerator

logger = logging.getLogger(__name__)


def list_topics():
    topics_file = Path(__file__).parent / "assets" / "topics_list.txt"
    if topics_file.exists():
        with open(topics_file, "r") as f:
            topics = [line.strip() for line in f if line.strip()]
        print("\n📋 Available Legal Right Topics:\n")
        for i, topic in enumerate(topics, 1):
            print(f" {i:2}. {topic}")
        print('\nUsage: medkit-legal generate "Topic Name"')
    else:
        print("Topics list not found.")


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="MedKit Legal - Patient Legal Rights Information Generator."
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
    parser.add_argument(
        "-u",
        "--user-name",
        default="anonymous",
        help="Name of the user for the filename.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Legal subcommands")

    # 1. Generate
    gen_p = subparsers.add_parser(
        "generate", help="Generate legal rights information for a topic"
    )
    gen_p.add_argument(
        "topic",
        help="Legal right topic (e.g., 'Informed Consent') or file path containing topics.",
    )
    gen_p.add_argument(
        "-c",
        "--country",
        default="India",
        help="The country/jurisdiction for the legal rights (e.g., 'USA', 'UK', 'India').",
    )

    # 2. List
    subparsers.add_parser("ls", help="List available legal right topics")

    return parser.parse_args()


def main():
    args = get_user_arguments()

    if args.command == "ls" or (not args.command and len(sys.argv) == 1):
        list_topics()
        return 0

    if not args.command:
        print("Use 'ls' to see available topics or 'generate' to create information.")
        return 1

    configure_logging(
        log_file="legal_rights.log", verbosity=args.verbosity, enable_console=True
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Only treat as a file path if it's reasonably short and exists
    items = [args.topic]
    if len(args.topic) < 255:
        input_path = Path(args.topic)
        if input_path.is_file():
            items = [line.strip() for line in open(input_path)]

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = LegalRightsGenerator(model_config)

        for item in tqdm(items, desc="Generating"):
            result = generator.generate_text(
                topic=item, country=args.country, structured=args.structured
            )
            if result:
                generator.save(result, output_dir, user_name=args.user_name)

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
