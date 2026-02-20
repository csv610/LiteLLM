"""
article_reviewer_cli.py - Command-line interface for article reviewer

Provides CLI functionality for reviewing articles with detailed feedback
on deletions, modifications, and insertions.
"""

import sys
import json
import argparse
from pathlib import Path

from article_reviewer import ArticleReviewer

def cli(article_text, model_name=None, output_filename=None, input_filename=None):
    """Review an article and provide detailed feedback on deletions, modifications, and insertions.

    Args:
        article_text (str): The full text of the article to review
        model_name (str): The model to use for review
                         Default: 'gemini/gemini-2.5-flash'
        output_filename (str): Optional output filename for the review
        input_filename (str): The input filename to use as base for output filename
    """
    if model_name is None:
        model_name = "gemini/gemini-2.5-flash"

    reviewer = ArticleReviewer(model_name=model_name)
    review = reviewer.review(article_text)
    output_file = reviewer.save_review(review, output_filename=output_filename, input_filename=input_filename)
    reviewer.print_review(review)
    print(f"Full review saved to: {output_file}\n")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Review an article and provide detailed feedback on deletions, modifications, and insertions.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python article_reviewer_cli.py "path/to/article.txt"
  python article_reviewer_cli.py "path/to/article.txt" -m "gpt-4"
  python article_reviewer_cli.py "The history of computers..." -m "claude-3-sonnet"
        """
    )

    parser.add_argument(
        "article",
        help="The article text to review (can be file path or direct text)"
    )
    parser.add_argument(
        "-m", "--model",
        default=None,
        help="Model to use for review (default: 'gemini/gemini-2.5-flash')"
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output filename for the review (default: {input_filename}_review.json or article_review_{timestamp}.json)"
    )

    args = parser.parse_args()

    # Try to load from file first, otherwise treat as direct text
    article_text = args.article
    input_filename = None
    try:
        with open(args.article, 'r', encoding='utf-8') as f:
            input_filename = args.article
            if args.article.endswith('.json'):
                data = json.load(f)
                # Handle various JSON structures - look for common article fields
                if isinstance(data, dict):
                    # Try common article field names
                    for field in ['content', 'article', 'text', 'body', 'data']:
                        if field in data:
                            article_text = data[field]
                            break
                    else:
                        # If no known field found, use the whole JSON as text
                        article_text = json.dumps(data, indent=2)
                elif isinstance(data, list):
                    # If JSON is a list, concatenate items
                    article_text = '\n'.join(str(item) for item in data)
            elif args.article.endswith(('.md', '.markdown')):
                # For markdown files, read as-is
                article_text = f.read()
            else:
                article_text = f.read()
    except (FileNotFoundError, IsADirectoryError):
        # If file doesn't exist, treat input as direct article text
        article_text = args.article

    cli(article_text, args.model, args.output, input_filename)


if __name__ == "__main__":
    main()
