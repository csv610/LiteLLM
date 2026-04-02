"""Extract keywords from medical documents using structured LLM output."""

import json
import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import logging

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.logging_config import configure_logging

try:
    from .models import KeywordList, KeywordResult
    from .prompts import PromptBuilder
except (ImportError, ValueError):
    from models import KeywordList, KeywordResult
    from prompts import PromptBuilder


# Setup logging
log_file = Path(__file__).parent / "logs" / "keyword_extraction.log"
log_file.parent.mkdir(exist_ok=True)
configure_logging(log_file=str(log_file))
logger = logging.getLogger(__name__)


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
        try:
            # Build prompt for medical keyword extraction
            prompt = PromptBuilder.get_keyword_extraction_prompt(text)

            # Use LiteClient with structured output
            model_input = ModelInput(user_prompt=prompt, response_format=KeywordList)

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
