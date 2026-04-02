"""
cli_base.py - Shared CLI utilities for article reviewer
"""

import json
import argparse
from typing import Tuple, Optional

def get_base_parser(description: str) -> argparse.ArgumentParser:
    """Create a base argument parser with common arguments."""
    parser = argparse.ArgumentParser(
        description=description,
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
    
    return parser

def load_article_text(article_input: str) -> Tuple[str, Optional[str]]:
    """Load article text from a file path or return the input string directly.
    
    Args:
        article_input: File path or direct article text
        
    Returns:
        Tuple[str, Optional[str]]: (article_text, input_filename)
    """
    article_text = article_input
    input_filename = None
    
    try:
        with open(article_input, "r", encoding="utf-8") as f:
            input_filename = article_input
            if article_input.endswith(".json"):
                try:
                    data = json.load(f)
                    if isinstance(data, dict):
                        # Try common article field names
                        for field in ["content", "article", "text", "body", "data"]:
                            if field in data:
                                article_text = data[field]
                                break
                        else:
                            # If no known field found, use the whole JSON as text
                            article_text = json.dumps(data, indent=2)
                    elif isinstance(data, list):
                        # If JSON is a list, concatenate items
                        article_text = "\n".join(str(item) for item in data)
                except json.JSONDecodeError:
                    # If JSON parsing fails, read as plain text
                    f.seek(0)
                    article_text = f.read()
            else:
                # For markdown, txt, or unknown extensions, read as-is
                article_text = f.read()
    except (FileNotFoundError, IsADirectoryError, PermissionError):
        # If file doesn't exist or error occurs, treat input as direct article text
        article_text = article_input
        input_filename = None

    return article_text, input_filename
