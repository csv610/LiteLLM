"""
Article Reviewer - A comprehensive tool for reviewing articles with detailed feedback
on deletions, modifications, and insertions using LiteClient.
"""

import json
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

from .article_reviewer_models import (
    ArticleReviewModel,
)
from .article_reviewer_prompts import PromptBuilder
from app.ArticleReviewer.shared.utils import (
    save_review as _save_review,
    print_review as _print_review,
)


class ArticleReviewer:
    """A comprehensive tool for reviewing articles with detailed feedback."""

    def __init__(self, model_config: ModelConfig = None):
        """Initialize the ArticleReviewer with a specified model configuration.

        Args:
            model_config: The configuration for the model. 
                         If None, defaults to 'ollama/gemma3' with temperature 0.3.
        """
        if model_config is None:
            model_config = ModelConfig(model="ollama/gemma3", temperature=0.3)
            
        self.model_config = model_config
        self.model_name = model_config.model
        self.client = LiteClient(model_config=self.model_config)

    def review(self, article_text: str) -> ArticleReviewModel:
        """Review an article and provide detailed feedback.

        Args:
            article_text: The full text of the article to review

        Returns:
            ArticleReviewModel: Structured review with deletions, modifications, and insertions
        """
        prompt = PromptBuilder.create_review_prompt(article_text)

        model_input = ModelInput(user_prompt=prompt, response_format=ArticleReviewModel)
        response_content = self.client.generate_text(model_input=model_input)

        if isinstance(response_content, str):
            data = json.loads(response_content)
            review = ArticleReviewModel(**data)
        elif isinstance(response_content, ArticleReviewModel):
            review = response_content
        else:
            raise ValueError(f"Expected string or ArticleReviewModel response from model, got {type(response_content)}")

        # Filter out cosmetic empty line deletions
        review.deletions = [
            d for d in review.deletions
            if d.content.strip() != ""  # Remove deletions that are just empty lines
        ]

        # Recalculate total issues
        review.total_issues = len(review.deletions) + len(review.modifications) + len(review.insertions)

        return review

    def save_review(self, review: ArticleReviewModel, output_filename: str = None, input_filename: str = None, output_dir: str = "outputs") -> str:
        """Save the review to a JSON file. delegates to shared.utils."""
        return _save_review(review, output_filename, input_filename, output_dir)

    def print_review(self, review: ArticleReviewModel) -> None:
        """Print a formatted review report to the console. delegates to shared.utils."""
        _print_review(review)
