"""
article_reviewer_cli.py - Command-line interface for the LiteClient multi-stage article reviewer.
"""

import argparse
import asyncio

from lite.config import ModelConfig
from .article_reviewer_agents import MultiAgentReviewer
from .article_reviewer_utils import save_review, print_review

async def run_review(article_text, model_name=None, output_filename=None, input_filename=None):
    """Run the multi-stage review."""
    if model_name is None:
        model_name = "ollama/gemma3"

    model_config = ModelConfig(model=model_name, temperature=0.3)
    reviewer = MultiAgentReviewer(model_config=model_config)
    
    print(f"Starting multi-stage review using model: {model_name}...")
    review = await reviewer.review(article_text)
    
    output_file = save_review(review, output_filename=output_filename, input_filename=input_filename)
    print_review(review)
    
    print(f"Full review saved to: {output_file}\n")


async def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Review an article using a LiteClient multi-stage workflow.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "article",
        help="The article text to review (can be file path or direct text)"
    )
    parser.add_argument(
        "-m", "--model",
        default=None,
        help="Model to use for review (default: 'ollama/gemma3')"
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output filename for the review"
    )

    args = parser.parse_args()

    # Try to load from file first
    article_text = args.article
    input_filename = None
    try:
        with open(args.article, 'r', encoding='utf-8') as f:
            input_filename = args.article
            article_text = f.read()
    except (FileNotFoundError, IsADirectoryError):
        pass

    await run_review(article_text, args.model, args.output, input_filename)


if __name__ == "__main__":
    asyncio.run(main())
