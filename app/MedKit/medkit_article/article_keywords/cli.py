import sys
import argparse
from pathlib import Path
from datetime import datetime
from tqdm import tqdm

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from .keyword_extraction import KeywordExtractor, logger
except (ImportError, ValueError):
    from keyword_extraction import KeywordExtractor, logger


def main() -> int:
    """Main entry point for keyword extraction CLI."""
    parser = argparse.ArgumentParser(
        description="Extract medical keywords and terms from text using LLM structured output",
        epilog="""
Examples:
  Extract from text:
    python cli.py -t "Patient has hypertension and diabetes"

  Extract from file:
    python cli.py -f medical_notes.txt
    python cli.py -f conditions.json
    python cli.py -f symptoms.md

  Use different model:
    python cli.py -f data.txt -m gemini/gemini-2.0-flash-exp

Output is saved to ./outputs/ directory as JSON.
JSON arrays are processed as separate items with individual keyword lists.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Input options (mutually exclusive: either text or file)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "-t",
        "--text",
        help="Direct text input to extract keywords from"
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

    args = parser.parse_args()

    try:
        # Initialize extractor
        extractor = KeywordExtractor(model=args.model)

        # Load input items
        items = extractor.load_file(args.file) if args.file else [{"id": "1", "text": args.text}]

        # Setup output directory and file path
        output_dir = Path(__file__).parent / "outputs"
        output_dir.mkdir(exist_ok=True)

        model_name = args.model.replace("/", "_")
        if args.file:
            base = Path(args.file).stem
            filename = f"{base}_keywords_{model_name}.json"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_keywords_{model_name}.json"

        output_file = output_dir / filename

        # Load existing results
        all_results = extractor.load_results(output_file)
        existing_ids = {r["id"] for r in all_results}

        # Process items
        for item in tqdm(items, desc="Extracting keywords"):
            # Skip already processed items
            if item["id"] in existing_ids:
                print(f"Item {item['id']}: Keywords already extracted, skipping...")
                logger.info(f"Skipped item {item['id']} - keywords already present")
                continue

            result = extractor.extract_keywords(item["text"], item["id"])
            if result:
                all_results.append(result)

                # Print to console
                print(f"\nItem {item['id']}:")
                print(f"Keywords ({len(result['keywords'])}):")
                for kw in result["keywords"]:
                    print(f"  - {kw}")

        # Save all results at once
        extractor.save_results(all_results, output_file)
        print(f"\nResults saved to: {output_file}")
        return 0

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
