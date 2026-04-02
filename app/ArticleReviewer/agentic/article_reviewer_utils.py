"""
article_reviewer_utils.py - Utility functions for article reviewer
"""

import json
import time
import os
from pathlib import Path
from .article_reviewer_models import ArticleReviewModel, ModelOutput

def save_review(output: ModelOutput, output_filename: str = None, input_filename: str = None, output_dir: str = "outputs") -> str:
    """Save the review artifact to files (.md and .json).

    Args:
        output: The ModelOutput artifact
        output_filename: Optional base filename for the output files.
        input_filename: The input filename to use as base for output filename.
        output_dir: The directory where the output file should be saved. Default is "outputs".

    Returns:
        str: The path to the saved Markdown file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    if output_filename is None:
        if input_filename:
            base_name = Path(input_filename).stem
            output_filename = f"{base_name}_review"
        else:
            output_filename = f"article_review_{int(time.time())}"
    
    # Final paths
    md_path = os.path.join(output_dir, f"{output_filename}.md")
    json_path = os.path.join(output_dir, f"{output_filename}.json")

    # Save Markdown
    if output.markdown:
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(output.markdown)

    # Save Data (JSON)
    if output.data:
        data_to_save = {
            "data": output.data.model_dump() if hasattr(output.data, 'model_dump') else output.data,
            "metadata": output.metadata
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4)

    return md_path

def print_review(output: ModelOutput) -> None:
    """Print the synthesized Markdown review to the console."""
    print(f"\n{'='*80}")
    print("MULTI-AGENT ARTICLE REVIEW REPORT")
    print(f"{'='*80}\n")
    
    if output.markdown:
        print(output.markdown)
    else:
        print("No Markdown synthesis available.")
        if output.data:
            print(f"Structured Data Score: {output.data.score}/100")
            print(f"Summary: {output.data.summary}")

    print(f"\n{'='*80}\n")
