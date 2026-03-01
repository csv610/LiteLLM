import sys
import argparse
import json
import logging
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from .article_review import ArticleReviewer
except (ImportError, ValueError):
    from article_review import ArticleReviewer
from lite.logging_config import configure_logging

# Setup logging
log_file = Path(__file__).parent / "logs" / "review.log"
log_file.parent.mkdir(exist_ok=True)
configure_logging(log_file=str(log_file))
logger = logging.getLogger(__name__)

def main() -> int:
    """Main entry point for medical article review CLI."""
    parser = argparse.ArgumentParser(
        description="Review a medical article using LLM structured output",
        epilog="""
Example:
  python article_review_cli.py -f article.md -m gemini/gemini-2.0-flash-exp

Output is saved to ./outputs/ directory as JSON.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "-f", "--file", 
        required=True, 
        help="Path to the article file (.txt, .md, .json)"
    )
    parser.add_argument(
        "-m", "--model", 
        default="ollama/gemma3", 
        help="Model identifier for LiteClient (default: %(default)s)"
    )

    args = parser.parse_args()

    try:
        # Initialize reviewer
        reviewer = ArticleReviewer(model=args.model)

        # Load article
        logger.info(f"Loading article: {args.file}")
        text = reviewer.load_file(args.file)

        # Perform review
        review = reviewer.review_article(text)

        if not review:
            print("Review failed. Check logs for details.")
            return 1

        # Setup output directory
        output_dir = Path(__file__).parent / "outputs"
        output_dir.mkdir(exist_ok=True)

        model_name = args.model.replace("/", "_")
        base = Path(args.file).stem
        filename = f"review_{base}_{model_name}.json"
        output_file = output_dir / filename

        # Save results
        result_dict = review.model_dump()
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)

        # Print to console
        print(f"\n--- Article Review: {review.title} ---\n")
        
        print(f"Summary:\n{review.summary}\n")
        
        print(f"Strengths:\n  - " + "\n  - ".join(review.strengths))
        print(f"Weaknesses:\n  - " + "\n  - ".join(review.weaknesses))
        
        print(f"\nClinical Implications:\n{review.clinical_implications}\n")
        print(f"Overall Quality: {review.overall_quality}\n")
        
        print(f"Full results saved to: {output_file}")
        return 0

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
