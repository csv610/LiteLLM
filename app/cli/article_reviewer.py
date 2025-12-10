"""
Article Reviewer - A comprehensive tool for reviewing articles with detailed feedback
on deletions, modifications, and insertions using LiteClient.
"""

import sys
import json
import argparse
import time
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydantic import BaseModel, Field
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput


class DeleteModel(BaseModel):
    """Model for content that should be removed from the article"""
    line_number: int = Field(..., description="The line number where the content to be deleted is located")
    content: str = Field(..., description="The specific phrase or sentence that should be deleted")
    reason: str = Field(..., description="Clear explanation of why this content should be removed")
    severity: str = Field(..., description="Severity level: 'low', 'medium', 'high', or 'critical'")


class ModifyModel(BaseModel):
    """Model for content that should be modified or improved"""
    line_number: int = Field(..., description="The line number of the content to be modified")
    original_content: str = Field(..., description="The original phrase or sentence")
    suggested_modification: str = Field(..., description="The improved version of the content")
    reason: str = Field(..., description="Explanation of why this modification improves the article")
    severity: str = Field(..., description="Severity level: 'low', 'medium', 'high', or 'critical'")


class InsertModel(BaseModel):
    """Model for content that should be added to the article"""
    line_number: int = Field(..., description="The line number after which content should be inserted")
    suggested_content: str = Field(..., description="The content that should be added")
    reason: str = Field(..., description="Explanation of why this content is necessary for completeness or accuracy")
    section: str = Field(..., description="The article section where this should be added (e.g., 'Introduction', 'Conclusion', 'Examples')")
    severity: str = Field(..., description="Severity level: 'low', 'medium', 'high', or 'critical'")


class ArticleReviewResponse(BaseModel):
    """Complete article review response"""
    score: int = Field(..., description="Overall quality score from 0-100")
    total_issues: int = Field(..., description="Total number of issues found (deletions + modifications + insertions)")
    summary: str = Field(..., description="Brief overall assessment of the article quality")
    deletions: list[DeleteModel] = Field(default=[], description="List of content to remove")
    modifications: list[ModifyModel] = Field(default=[], description="List of content to modify")
    insertions: list[InsertModel] = Field(default=[], description="List of content to insert")
    proofreading_rules_applied: list[str] = Field(default=[], description="List of proofreading rule categories that were applied during the review")


class ArticleReviewer:
    """A comprehensive tool for reviewing articles with detailed feedback."""

    PROOFREADING_RULES = {
        "Grammar & Syntax": {
            "subject_verb_agreement": "Verify subject and verb agreement in all sentences",
            "tense_consistency": "Maintain consistent verb tense throughout the article",
            "pronoun_reference": "Ensure pronouns clearly refer to their antecedents",
            "article_usage": "Correct usage of articles (a, an, the)",
            "preposition_usage": "Verify proper preposition usage"
        },
        "Style & Clarity": {
            "active_voice": "Prefer active voice over passive voice where appropriate",
            "sentence_clarity": "Ensure sentences are clear and concise",
            "redundancy": "Eliminate redundant words and phrases",
            "jargon": "Explain technical terms or avoid unnecessary jargon",
            "word_choice": "Verify precise and appropriate word choices",
            "sentence_length": "Maintain appropriate sentence length to avoid confusion"
        },
        "Formatting & Punctuation": {
            "punctuation": "Correct punctuation usage (commas, periods, semicolons, etc.)",
            "capitalization": "Verify correct capitalization of proper nouns and sentence starts",
            "quotation_marks": "Ensure proper quotation mark usage and consistency",
            "apostrophe_usage": "Correct apostrophe usage in contractions and possessives",
            "numbering": "Consistent formatting of numbers (spelled out vs. digits)",
            "hyphenation": "Correct hyphenation of compound words"
        },
        "Content & Structure": {
            "fact_accuracy": "Verify factual accuracy of claims and statements",
            "sources": "Include proper citations and sources where needed",
            "completeness": "Ensure article covers all necessary aspects of the topic",
            "logical_flow": "Verify logical progression and coherence of ideas",
            "relevance": "Ensure all content is relevant to the article's purpose",
            "introduction": "Article has clear introduction with thesis or purpose statement",
            "conclusion": "Article has meaningful conclusion summarizing key points"
        },
        "Consistency": {
            "terminology": "Use consistent terminology throughout the article",
            "formatting_style": "Maintain consistent formatting style across all sections",
            "tone": "Maintain consistent tone appropriate for the audience",
            "section_structure": "Maintain consistent structure across similar sections"
        }
    }

    def __init__(self, model_name: str = "gemini/gemini-2.5-flash"):
        """Initialize the ArticleReviewer with a specified model.

        Args:
            model_name: The model to use for review (default: 'gemini/gemini-2.5-flash')
        """
        self.model_name = model_name
        self.model_config = ModelConfig(model=model_name, temperature=0.3)
        self.client = LiteClient(model_config=self.model_config)

    def review(self, article_text: str) -> ArticleReviewResponse:
        """Review an article and provide detailed feedback.

        Args:
            article_text: The full text of the article to review

        Returns:
            ArticleReviewResponse: Structured review with deletions, modifications, and insertions
        """
        prompt = f"""You are an expert article reviewer and proofreader. Review the following article comprehensively.

ARTICLE TO REVIEW:
<article>
{article_text}
</article>

PROOFREADING RULES TO APPLY:
{json.dumps(self.PROOFREADING_RULES, indent=2)}

INSTRUCTIONS:
1. Review the article against all proofreading rule categories above
2. Identify specific issues and categorize them as deletions, modifications, or insertions
3. For each issue, provide:
   - The exact line number
   - The complete, full text (for deletions and modifications)
   - Clear, specific, and actionable reason
   - Severity level (low, medium, high, critical)
4. ALL suggestions must be COMPLETE and UNAMBIGUOUS:
   - Never provide partial or fragmented text
   - Include full sentences or phrases, not excerpts
   - Make suggestions ready to implement without additional interpretation
   - Be specific about what to do, not vague

DELETION SUGGESTIONS:
- Remove redundant phrases, unnecessary words, or irrelevant content
- Flag repeated information
- Remove unsupported claims or outdated references
- REQUIREMENT: Provide the COMPLETE phrase or sentence to be deleted
NOTE: Do NOT include empty lines or whitespace issues as deletions - these are cosmetic and not substantive.

MODIFICATION SUGGESTIONS:
- Improve clarity and readability
- Fix grammar, punctuation, and style issues
- Enhance word choice for precision
- Convert passive to active voice where appropriate
- Break up overly long sentences
- REQUIREMENT: Provide the COMPLETE original text and COMPLETE suggested replacement (full sentences or phrases, not fragments)

INSERTION SUGGESTIONS:
- Add missing context or explanations
- Include citations where needed
- Add examples for clarity
- Include introduction/conclusion if missing
- Add transitions between ideas
- REQUIREMENT: Provide COMPLETE, ready-to-use content for insertion (full sentences or paragraphs)

SCORING GUIDELINES:
- 90-100: Excellent - minimal issues, professional quality
- 80-89: Good - well-written with minor improvements
- 70-79: Fair - several issues that should be addressed
- 60-69: Poor - significant issues requiring revision
- Below 60: Very Poor - substantial revision needed

Provide a fair assessment based on the total number and severity of issues found. Focus on substantive content issues, not cosmetic formatting."""

        model_input = ModelInput(user_prompt=prompt, response_format=ArticleReviewResponse)
        response_content = self.client.generate_text(model_input=model_input)

        if isinstance(response_content, str):
            data = json.loads(response_content)
            review = ArticleReviewResponse(**data)

            # Filter out cosmetic empty line deletions
            review.deletions = [
                d for d in review.deletions
                if d.content.strip() != ""  # Remove deletions that are just empty lines
            ]

            # Recalculate total issues
            review.total_issues = len(review.deletions) + len(review.modifications) + len(review.insertions)

            return review
        else:
            raise ValueError("Expected string response from model")

    def save_review(self, review: ArticleReviewResponse, output_filename: str = None, input_filename: str = None) -> str:
        """Save the review to a JSON file.

        Args:
            review: The ArticleReviewResponse to save
            output_filename: Optional filename for the output file. If not provided, uses input_filename.
            input_filename: The input filename to use as base for output filename.

        Returns:
            str: The path to the saved file
        """
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

        with open(output_filename, 'w') as f:
            json.dump(review.model_dump(), f, indent=4)

        return output_filename

    def print_review(self, review: ArticleReviewResponse) -> None:
        """Print a formatted review report to the console.

        Args:
            review: The ArticleReviewResponse to print
        """
        print(f"\n{'='*80}")
        print("ARTICLE REVIEW REPORT")
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Review an article and provide detailed feedback on deletions, modifications, and insertions.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python article_reviewer.py "path/to/article.txt"
  python article_reviewer.py "path/to/article.txt" -m "gpt-4"
  python article_reviewer.py "The history of computers..." -m "claude-3-sonnet"
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
