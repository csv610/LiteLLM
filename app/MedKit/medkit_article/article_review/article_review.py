"""Review a single medical article."""

import json
import logging
from pathlib import Path
from typing import Optional

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
try:
    from .article_review_models import ArticleReview
    from .article_review_prompts import PromptBuilder
except (ImportError, ValueError):
    from article_review_models import ArticleReview
    from article_review_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class ArticleReviewer:
    """Review an article and evaluate its strengths, weaknesses, and clinical implications."""

    def __init__(self, model: str = "ollama/gemma3"):
        """
        Initialize the ArticleReviewer.

        Args:
            model: LiteClient model to use for review
        """
        self.model = model
        
        try:
            model_config = ModelConfig(model=model, temperature=0.2)
            self.client = LiteClient(model_config=model_config)
            logger.info(f"Reviewer client created with model: {model}")
        except Exception as e:
            logger.error(f"Failed to create reviewer client: {e}")
            raise

    def load_file(self, file_path: str) -> str:
        """Load article text from a file."""
        path = Path(file_path).expanduser()
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
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

    def review_article(
        self, 
        article_text: str
    ) -> Optional[ArticleReview]:
        """
        Review a single medical article.

        Args:
            article_text: Text of the article

        Returns:
            ArticleReview object or None if failed
        """
        try:
            logger.info("Generating article review...")
            prompt = PromptBuilder.get_review_prompt(article_text)
            model_input = ModelInput(
                user_prompt=prompt,
                response_format=ArticleReview
            )
            response = self.client.generate_text(model_input=model_input)
            return response
        except Exception as e:
            logger.error(f"Error during review: {e}")
            return None
