"""
article_reviewer_utils.py - Utility functions for article reviewer
"""

from app.ArticleReviewer.shared.utils import (
    save_review as _save_review,
    print_review as _print_review
)
from app.ArticleReviewer.shared.models import ModelOutput

def save_review(output: ModelOutput, output_filename: str = None, input_filename: str = None, output_dir: str = "outputs") -> str:
    """Save the review artifact to files (.md and .json). delegates to shared.utils."""
    return _save_review(output, output_filename, input_filename, output_dir)

def print_review(output: ModelOutput) -> None:
    """Print the synthesized Markdown review to the console. delegates to shared.utils."""
    _print_review(output)
