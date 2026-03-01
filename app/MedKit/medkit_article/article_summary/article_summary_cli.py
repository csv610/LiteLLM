import sys
import argparse
import json
from pathlib import Path
from datetime import datetime
from tqdm import tqdm

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from .article_summary import ArticleSummarizer, logger
except (ImportError, ValueError):
    from article_summary import ArticleSummarizer, logger


def main() -> int:
    """Main entry point for medical article summarization CLI."""
    parser = argparse.ArgumentParser(
        description="Summarize medical articles using LLM structured output",
        epilog="""
Examples:
  Summarize an article:
    python article_summary_cli.py -f article.md

  Summarize with custom chunking:
    python article_summary_cli.py -f large_article.txt --chunk-size 2000 --overlap 0.2

  Use different model:
    python article_summary_cli.py -f data.txt -m gemini/gemini-2.0-flash-exp

Output is saved to ./outputs/ directory as JSON.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Input options (mutually exclusive: either text or file)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "-t",
        "--text",
        help="Direct text input to summarize"
    )
    input_group.add_argument(
        "-f",
        "--file",
        help="Input file path (.txt for plain text, .json for JSON arrays, .md for markdown)",
    )

    parser.add_argument(
        "-m",
        "--model",
        default="ollama/gemma3",
        help="Model identifier for LiteClient (default: %(default)s)",
    )

    parser.add_argument(
        "--chunk-size",
        type=int,
        default=100000,
        help="Maximum characters per chunk for summarization (default: %(default)s)"
    )
    parser.add_argument(
        "--overlap",
        type=float,
        default=0.1,
        help="Ratio of overlap between chunks (default: %(default)s)"
    )

    args = parser.parse_args()

    try:
        # Initialize summarizer
        summarizer = ArticleSummarizer(model=args.model)

        # Load input items
        items = summarizer.load_file(args.file) if args.file else [{"id": "1", "text": args.text}]

        # Setup output directory
        output_dir = Path(__file__).parent / "outputs"
        output_dir.mkdir(exist_ok=True)

        model_name = args.model.replace("/", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Decide output file path
        if args.file:
            base = Path(args.file).stem
            filename = f"{base}_summary_{model_name}.json"
        else:
            filename = f"{timestamp}_summary_{model_name}.json"

        output_file = output_dir / filename

        # Load existing results (if file exists)
        all_results = []
        if output_file.exists():
            try:
                with open(output_file, "r", encoding="utf-8") as f:
                    all_results = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        existing_ids = {r["id"] for r in all_results}

        # Process items
        for item in tqdm(items, desc="Summarizing"):
            # Skip already processed items
            if item["id"] in existing_ids:
                print(f"Item {item['id']}: Already summarized, skipping...")
                continue

            summary = summarizer.summarize_article(
                item["text"], 
                chunk_size=args.chunk_size, 
                overlap_ratio=args.overlap
            )
            
            if summary:
                result = {
                    "id": item["id"],
                    "summary": summary
                }
                all_results.append(result)

                # Print to console
                print(f"\nItem {item['id']} Summary:\n{summary}\n")

        # Save all results
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
            
        print(f"\nResults saved to: {output_file}")
        return 0

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
