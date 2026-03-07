import argparse
import json
import logging
import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from .article_comparison import ArticleComparator
except (ImportError, ValueError):
    from article_comparison import ArticleComparator
from lite.logging_config import configure_logging

# Setup logging
log_file = Path(__file__).parent / "logs" / "comparison.log"
log_file.parent.mkdir(exist_ok=True)
configure_logging(log_file=str(log_file))
logger = logging.getLogger(__name__)


def main() -> int:
    """Main entry point for medical article comparison CLI."""
    parser = argparse.ArgumentParser(
        description="Compare two medical articles side-by-side using LLM structured output",
        epilog="""
Example:
  python cli.py -f1 article1.md -f2 article2.md -m gemini/gemini-2.0-flash-exp

Output is saved to ./outputs/ directory as JSON.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-f1",
        "--file1",
        required=True,
        help="Path to the first article file (.txt, .md, .json)",
    )
    parser.add_argument(
        "-f2",
        "--file2",
        required=True,
        help="Path to the second article file (.txt, .md, .json)",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="ollama/gemma3",
        help="Model identifier for LiteClient (default: %(default)s)",
    )

    args = parser.parse_args()

    try:
        # Initialize comparator
        comparator = ArticleComparator(model=args.model)

        # Load articles
        logger.info(f"Loading articles: {args.file1}, {args.file2}")
        text1 = comparator.load_file(args.file1)
        text2 = comparator.load_file(args.file2)

        # Perform comparison
        comparison = comparator.compare_articles(text1, text2)

        if not comparison:
            print("Comparison failed. Check logs for details.")
            return 1

        # Setup output directory
        output_dir = Path(__file__).parent / "outputs"
        output_dir.mkdir(exist_ok=True)

        model_name = args.model.replace("/", "_")
        base1 = Path(args.file1).stem
        base2 = Path(args.file2).stem
        filename = f"comparison_{base1}_{base2}_{model_name}.json"
        output_file = output_dir / filename

        # Save results
        result_dict = comparison.model_dump()
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)

        print(f"Comparison results saved to: {output_file}")
        return 0

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
