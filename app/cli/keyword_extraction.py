"""Extract keywords from medical documents using structured LLM output."""

import sys
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime

from tqdm import tqdm

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydantic import BaseModel, Field
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from logging_util import setup_logging


# Setup logging
log_file = Path(__file__).parent / "logs" / "keyword_extraction.log"
logger = setup_logging(str(log_file))


class KeywordList(BaseModel):
    """Structured keyword output from LLM."""

    keywords: list[str] = Field(description="List of medical keywords and important terms")


class KeywordResult(BaseModel):
    """Result for a single item extraction."""

    id: str = Field(description="Identifier for the item")
    keywords: list[str] = Field(description="Extracted keywords")


class KeywordExtractor:
    """Extract keywords from documents using LiteClient with structured output."""

    def __init__(self, model: str = "ollama/gemma3"):
        """
        Initialize the KeywordExtractor.

        Args:
            model: LiteClient model to use for extraction
        """
        self.model = model

        try:
            model_config = ModelConfig(model=model, temperature=0.2)
            self.client = LiteClient(model_config=model_config)
            logger.info(f"Client created with model: {model}")
        except Exception as e:
            logger.error(f"Failed to create client: {e}")
            raise

    def _extract_text_from_object(self, obj) -> str:
        """
        Recursively extract all text values from nested objects.

        Args:
            obj: Dictionary, list, or string to extract text from

        Returns:
            Concatenated text content
        """
        texts = []

        if isinstance(obj, dict):
            for value in obj.values():
                texts.append(self._extract_text_from_object(value))
        elif isinstance(obj, list):
            for item in obj:
                texts.append(self._extract_text_from_object(item))
        elif isinstance(obj, str):
            texts.append(obj)

        return " ".join(filter(None, texts))

    def _parse_text_file(self, file_path: str) -> list[dict]:
        """Parse plain text file and return as single item."""
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        return [{"id": "1", "text": text}]

    def _parse_json_file(self, file_path: str) -> list[dict]:
        """Parse JSON file and return items with their extracted text."""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        items = []

        if isinstance(data, list):
            # Multi-item file - process each separately
            for i, item in enumerate(data):
                text = self._extract_text_from_object(item)
                items.append({"id": str(i + 1), "text": text})
                logger.debug(f"Parsed item {i + 1}")
        else:
            # Single object
            text = self._extract_text_from_object(data)
            items.append({"id": "1", "text": text})
            logger.debug("Parsed single object from JSON")

        logger.info(f"Loaded {len(items)} items from JSON file")
        return items

    def _parse_markdown_file(self, file_path: str) -> list[dict]:
        """Parse Markdown file and return as single item."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return [{"id": "1", "text": content}]

    def load_file(self, file_path: str) -> list[dict]:
        """
        Auto-detect and parse file based on extension.

        Args:
            file_path: Path to file (.txt, .json, or .md)

        Returns:
            List of items with extracted text
        """
        file_path = str(Path(file_path).expanduser())

        if file_path.endswith(".json"):
            return self._parse_json_file(file_path)
        elif file_path.endswith(".md"):
            return self._parse_markdown_file(file_path)
        else:
            # Default to plain text
            return self._parse_text_file(file_path)

    def extract_keywords(self, text: str, item_id: str = "1") -> dict:
        """
        Extract keywords using structured LLM output.

        Args:
            text: Text to extract keywords from
            item_id: Identifier for this item

        Returns:
            Dictionary with keywords and metadata, or None on error
        """
        # Create prompt for medical keyword extraction
        prompt = """Extract all medical keywords and important terms from this text.
Return ONLY medical terminology including:
- Diseases, conditions, and syndromes
- Symptoms and clinical findings
- Treatments, medications, and procedures
- Anatomical terms
- Diagnostic tests and imaging findings

Focus on specific medical terms, not generic descriptions. Be precise and clinical.

Text:
""" + text

        try:
            # Use LiteClient with structured output
            model_input = ModelInput(
                user_prompt=prompt,
                response_format=KeywordList
            )

            response = self.client.generate_text(model_input=model_input)
            keywords = response.keywords

            # Deduplicate, sort, and filter empty strings
            keywords = sorted(set(kw.strip().lower() for kw in keywords if kw.strip()))

            logger.info(f"Extracted {len(keywords)} keywords for item {item_id}")

            return KeywordResult(
                id=item_id,
                keywords=keywords,
            ).model_dump()

        except Exception as e:
            logger.error(f"Failed to extract keywords for item {item_id}: {e}")
            return None

    def load_results(self, output_file: Path) -> list[dict]:
        """
        Load existing results from file.

        Args:
            output_file: Path to the output file

        Returns:
            List of existing results or empty list
        """
        if not output_file.exists():
            return []

        try:
            with open(output_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def save_results(self, results: list[dict], output_file: Path) -> None:
        """
        Save results to file.

        Args:
            results: List of results to save
            output_file: Path to the output file
        """
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

def main() -> int:
    """Main entry point for keyword extraction CLI."""
    parser = argparse.ArgumentParser(
        description="Extract medical keywords and terms from text using LLM structured output",
        epilog="""
Examples:
  Extract from text:
    python keyword_extraction.py -t "Patient has hypertension and diabetes"

  Extract from file:
    python keyword_extraction.py -f medical_notes.txt
    python keyword_extraction.py -f conditions.json
    python keyword_extraction.py -f symptoms.md

  Use different model:
    python keyword_extraction.py -f data.txt -m gemini/gemini-2.0-flash-exp

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
