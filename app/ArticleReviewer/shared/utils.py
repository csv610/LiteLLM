"""
utils.py - Shared utility functions for article reviewer
"""

import json
import time
import os
from pathlib import Path
from typing import Union, Optional
from .models import ArticleReviewModel, ModelOutput

def save_review(
    review: Union[ArticleReviewModel, ModelOutput], 
    output_filename: Optional[str] = None, 
    input_filename: Optional[str] = None, 
    output_dir: str = "outputs"
) -> str:
    """Save the review to files. Handles both ArticleReviewModel and ModelOutput.

    Args:
        review: The review object to save
        output_filename: Optional base filename for the output files.
        input_filename: The input filename to use as base for output filename.
        output_dir: The directory where the output file should be saved. Default is "outputs".

    Returns:
        str: The path to the primary saved file (Markdown if available, otherwise JSON)
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    if output_filename is None:
        if input_filename:
            base_name = Path(input_filename).stem
            output_filename = f"{base_name}_review"
        else:
            output_filename = f"article_review_{int(time.time())}"
    
    # Remove .json or .md extension if present in output_filename to use as base
    if output_filename.endswith(('.json', '.md')):
        output_filename = Path(output_filename).stem

    # Determine paths
    md_path = os.path.join(output_dir, f"{output_filename}.md")
    json_path = os.path.join(output_dir, f"{output_filename}.json")

    # Case 1: ModelOutput (agentic)
    if isinstance(review, ModelOutput):
        # Save Markdown
        if review.markdown:
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(review.markdown)

        # Save Data (JSON)
        if review.data:
            data_to_save = {
                "data": review.data.model_dump() if hasattr(review.data, 'model_dump') else review.data,
                "metadata": review.metadata
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4)
        
        return md_path if review.markdown else json_path

    # Case 2: ArticleReviewModel (non-agentic)
    else:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(review.model_dump(), f, indent=4)
        return json_path

def print_review(review: Union[ArticleReviewModel, ModelOutput]) -> None:
    """Print a formatted review report to the console."""
    print(f"\n{'='*80}")
    print("ARTICLE REVIEW REPORT")
    print(f"{'='*80}\n")

    if isinstance(review, ModelOutput):
        if review.markdown:
            print(review.markdown)
        else:
            if review.data:
                _print_article_review_model(review.data)
            else:
                print("No content available to display.")
    else:
        _print_article_review_model(review)

    print(f"\n{'='*80}\n")

def _print_article_review_model(review: ArticleReviewModel) -> None:
    """Helper to print the structured ArticleReviewModel."""
    print(f"Overall Score: {review.score}/100")
    print(f"Summary: {review.summary}\n")
    print(f"Total Issues Found: {review.total_issues}")
    print(f"  - Deletions: {len(review.deletions)}")
    print(f"  - Modifications: {len(review.modifications)}")
    print(f"  - Insertions: {len(review.insertions)}")

    # Print deletions
    if review.deletions:
        print(f"{'─'*80}")
        print("DELETIONS (Content to Remove)")
        print(f"{'─'*80}")
        for deletion in review.deletions:
            print(f"\n[{deletion.severity.upper()}] Line {deletion.line_number}")
            print(f"Content: \"{deletion.content}\"")
            print(f"Reason: {deletion.reason}")

    # Print modifications
    if review.modifications:
        print(f"\n{'─'*80}")
        print("MODIFICATIONS (Content to Improve)")
        print(f"{'─'*80}")
        for mod in review.modifications:
            print(f"\n[{mod.severity.upper()}] Line {mod.line_number}")
            print(f"Original: \"{mod.original_content}\"")
            print(f"Suggested: \"{mod.suggested_modification}\"")
            print(f"Reason: {mod.reason}")

    # Print insertions
    if review.insertions:
        print(f"\n{'─'*80}")
        print("INSERTIONS (Content to Add)")
        print(f"{'─'*80}")
        for insertion in review.insertions:
            print(f"\n[{insertion.severity.upper()}] After Line {insertion.line_number}")
            print(f"Section: {insertion.section}")
            print(f"Suggested Content: \"{insertion.suggested_content}\"")
            print(f"Reason: {insertion.reason}")
