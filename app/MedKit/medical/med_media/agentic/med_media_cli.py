import argparse
import logging
import sys
from pathlib import Path

# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from lite.config import ModelConfig
from lite.logging_config import configure_logging

try:
    from .med_media import MedicalMediaGenerator
except (ImportError, ValueError):
    from medical.med_media.agentic.med_media import MedicalMediaGenerator

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="MedKit Media CLI - Search, download, and analyze medical media."
    )

    # Global arguments
    parser.add_argument(
        "-m", "--model", default="ollama/gemma3", help="Model to use for AI analysis."
    )
    parser.add_argument(
        "-d",
        "--output-dir",
        default="outputs/media",
        help="Output directory for results.",
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
        "-s", "--structured", action="store_true", help="Use structured output (JSON)."
    )

    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Media tool subcommands"
    )

    # Image Download
    images_p = subparsers.add_parser(
        "images", help="Search and download medical images"
    )
    images_p.add_argument(
        "query", help="Search query (e.g., 'acne vulgaris', 'heart anatomy')"
    )
    images_p.add_argument(
        "-n", "--num", type=int, default=3, help="Number of images to download"
    )
    images_p.add_argument(
        "--size",
        choices=["Small", "Medium", "Large", "Wallpaper"],
        default="Medium",
        help="Image size filter",
    )

    # Video Search
    videos_p = subparsers.add_parser("videos", help="Search for medical videos")
    videos_p.add_argument(
        "query",
        help="Search query (e.g., 'laparoscopic surgery', 'diabetes education')",
    )
    videos_p.add_argument(
        "-n", "--num", type=int, default=5, help="Number of results to list"
    )

    # Caption Generation
    caption_p = subparsers.add_parser(
        "caption", help="Generate professional medical caption"
    )
    caption_p.add_argument("topic", help="Topic for the caption")
    caption_p.add_argument(
        "-t",
        "--type",
        default="image",
        choices=["image", "x-ray", "mri", "ct", "pathology"],
        help="Media type context",
    )

    # Summary Generation
    summary_p = subparsers.add_parser(
        "summary", help="Generate medical summary for educational content"
    )
    summary_p.add_argument("topic", help="Topic for the summary")
    summary_p.add_argument(
        "-t",
        "--type",
        default="video",
        choices=["video", "article", "lecture"],
        help="Media type context",
    )

    args = parser.parse_args()

    # Configure logging
    configure_logging(
        log_file="medkit_media.log", verbosity=args.verbosity, enable_console=True
    )
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model_config = ModelConfig(model=args.model, temperature=0.2)
    generator = MedicalMediaGenerator(model_config)

    try:
        if args.command == "images":
            print(
                f"🔍 Searching and downloading {args.num} images for: {args.query}..."
            )
            downloaded = generator.download_images(
                args.query, args.num, args.size, output_dir / "images"
            )
            for path in downloaded:
                print(f"✓ Saved: {path}")

        elif args.command == "videos":
            print(f"🔍 Searching for medical videos: {args.query}...")
            results = generator.search_videos(args.query, args.num)
            if not results:
                print("No videos found.")
            else:
                for res in results:
                    print(f"- {res['title']} ({res['duration']}): {res['url']}")

        elif args.command == "caption":
            print(f"✍️ Generating caption for {args.type}: {args.topic}...")
            res = generator.generate_caption(
                args.topic, args.type, structured=args.structured
            )
            if res:
                path = generator.save(res, output_dir, suffix="caption")
                print(f"✓ Caption generated and saved to: {path}")

        elif args.command == "summary":
            print(f"✍️ Generating summary for {args.type}: {args.topic}...")
            res = generator.generate_summary(
                args.topic, args.type, structured=args.structured
            )
            if res:
                path = generator.save(res, output_dir, suffix="summary")
                print(f"✓ Summary generated and saved to: {path}")

    except Exception as e:
        logger.error(f"Error executing command '{args.command}': {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
