"""
article_reviewer_utils.py - Utility functions for article reviewer
"""

import json
import time
import os
from pathlib import Path
from article_reviewer_models import ArticleReviewModel

def save_review(review: ArticleReviewModel, output_filename: str = None, input_filename: str = None, output_dir: str = "outputs") -> str:
    """Save the review to a JSON file.

    Args:
        review: The ArticleReviewModel to save
        output_filename: Optional filename for the output file. If not provided, uses input_filename.
        input_filename: The input filename to use as base for output filename.
        output_dir: The directory where the output file should be saved. Default is "outputs".

    Returns:
        str: The path to the saved file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    if output_filename is None:
        if input_filename:
            # Extract base filename without extension
            base_name = Path(input_filename).stem
            output_filename = f"{base_name}_review.json"
        else:
            output_filename = f"article_review_{int(time.time())}.json"
    else:
        if not output_filename.endswith('.json'):
            output_filename = f"{output_filename}_review.json"

    # Final path should be in the output_dir
    # If output_filename is just a name, join it with output_dir
    # If output_filename has a path component, still place it in output_dir unless it's absolute
    if os.path.isabs(output_filename):
        output_path = output_filename
    else:
        file_name = os.path.basename(output_filename)
        output_path = os.path.join(output_dir, file_name)

    # Create the directory for output_path if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(review.model_dump(), f, indent=4)

    return output_path

def print_review(review: ArticleReviewModel) -> None:
    """Print a formatted review report to the console.

    Args:
        review: The ArticleReviewModel to print
    """
    print(f"\n{'='*80}")
    print("MULTI-AGENT ARTICLE REVIEW REPORT")
    print(f"{'='*80}\n")
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

    print(f"\n{'='*80}\n")
