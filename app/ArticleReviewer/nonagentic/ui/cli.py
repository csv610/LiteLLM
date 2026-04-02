"""
article_reviewer_cli.py - Command-line interface for article reviewer

Provides CLI functionality for reviewing articles with detailed feedback
on deletions, modifications, and insertions.
"""

import sys
from pathlib import Path

# Add the project root to sys.path
path = Path(__file__).parent
while path.name != "app" and path.parent != path:
    path = path.parent
if path.name == "app":
    root = path.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

from lite.config import ModelConfig  # noqa: E402
from app.ArticleReviewer.nonagentic.article_reviewer import ArticleReviewer  # noqa: E402
from app.ArticleReviewer.shared.cli_base import get_base_parser, load_article_text  # noqa: E402


def cli(article_text, model_name=None, output_filename=None, input_filename=None):
    """Review an article and provide detailed feedback on deletions, modifications, and insertions.

    Args:
        article_text (str): The full text of the article to review
        model_name (str): The model to use for review
                         Default: 'ollama/gemma3'
        output_filename (str): Optional output filename for the review
        input_filename (str): The input filename to use as base for output filename
    """
    if model_name is None:
        model_name = "ollama/gemma3"

    model_config = ModelConfig(model=model_name, temperature=0.3)
    reviewer = ArticleReviewer(model_config=model_config)
    review = reviewer.review(article_text)
    output_file = reviewer.save_review(
        review, output_filename=output_filename, input_filename=input_filename
    )
    reviewer.print_review(review)
    print(f"Full review saved to: {output_file}\n")


def main():
    """Main CLI entry point"""
    description = "Review an article and provide detailed feedback on deletions, modifications, and insertions."
    parser = get_base_parser(description)
    
    # Custom epilog
    parser.epilog = """
Examples:
  python article_reviewer_cli.py "path/to/article.txt"
  python article_reviewer_cli.py "path/to/article.txt" -m "gpt-4"
  python article_reviewer_cli.py "The history of computers..." -m "claude-3-sonnet"
    """

    args = parser.parse_args()

    article_text, input_filename = load_article_text(args.article)
    cli(article_text, args.model, args.output, input_filename)


if __name__ == "__main__":
    main()
