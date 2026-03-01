"""Compare two medical articles side-by-side."""

import json
import logging
from pathlib import Path
from typing import Optional

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
try:
    from .article_comparison_models import ComparisonResult
    from .article_comparison_prompts import PromptBuilder
except (ImportError, ValueError):
    from article_comparison_models import ComparisonResult
    from article_comparison_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class ArticleComparator:
    """Compare two articles and evaluate their strengths and weaknesses side-by-side."""

    def __init__(self, model: str = "ollama/gemma3"):
        """
        Initialize the ArticleComparator.

        Args:
            model: LiteClient model to use for comparison
        """
        self.model = model

        try:
            model_config = ModelConfig(model=model, temperature=0.2)
            self.client = LiteClient(model_config=model_config)
            logger.info(f"Comparator client created with model: {model}")
        except Exception as e:
            logger.error(f"Failed to create comparator client: {e}")
            raise

    def load_file(self, file_path: str) -> str:
        """Load article text from a file."""
        path = Path(file_path).expanduser()
        ext = path.suffix.lower()

        if ext == ".json":
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return self._extract_text_from_object(data)
        else:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()

    def _extract_text_from_object(self, obj) -> str:
        """Recursively extract all text values from nested objects."""
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

    def compare_articles(
        self, article1_text: str, article2_text: str
    ) -> Optional[ComparisonResult]:
        """
        Compare two articles side-by-side.

        Args:
            article1_text: Text of the first article
            article2_text: Text of the second article

        Returns:
            ComparisonResult object or None if failed
        """
        try:
            logger.info("Generating side-by-side comparison...")
            prompt = PromptBuilder.get_comparison_prompt(article1_text, article2_text)
            model_input = ModelInput(
                user_prompt=prompt, response_format=ComparisonResult
            )
            response = self.client.generate_text(model_input=model_input)
            return response
        except Exception as e:
            logger.error(f"Error during comparison: {e}")
            return None
