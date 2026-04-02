"""
optimize_models.py - Script to optimize Pydantic models for ArticleReviewer using DSPydantic with Ollama.
"""

import dspy
from dspy.teleprompt import BootstrapFewShot
from article_reviewer_models import (
    ArticleReviewModel,
)

# Configure DSPy to use Ollama
ollama_lm = dspy.Ollama(
    model="llama3",  # Change to your preferred Ollama model
    max_tokens=2000,
    temperature=0.3,  # Lower temperature for more consistent output
)
dspy.settings.configure(lm=ollama_lm)


def article_review_metric(example, pred, trace=None):
    """
    Validation metric for ArticleReviewModel.
    Checks that the review contains all required components with reasonable quality.
    """
    # Check required fields exist and are appropriate types
    if not isinstance(pred.score, int) or not (0 <= pred.score <= 100):
        return False

    if not isinstance(pred.total_issues, int) or pred.total_issues < 0:
        return False

    if not isinstance(pred.summary, str) or len(pred.summary.strip()) < 10:
        return False

    # Check that lists are actually lists
    if not isinstance(pred.deletions, list):
        return False
    if not isinstance(pred.modifications, list):
        return False
    if not isinstance(pred.insertions, list):
        return False
    if not isinstance(pred.proofreading_rules_applied, list):
        return False

    # Additional validation: total_issues should roughly match sum of lists
    actual_total = len(pred.deletions) + len(pred.modifications) + len(pred.insertions)
    if abs(actual_total - pred.total_issues) > 5:  # Allow some flexibility
        return False

    # Validate each item in the lists has required fields
    for deletion in pred.deletions:
        if not isinstance(deletion, dict) or not all(
            k in deletion for k in ["line_number", "content", "reason", "severity"]
        ):
            return False
        if deletion["severity"] not in ["low", "medium", "high", "critical"]:
            return False

    for modification in pred.modifications:
        if not isinstance(modification, dict) or not all(
            k in modification
            for k in [
                "line_number",
                "original_content",
                "suggested_modification",
                "reason",
                "severity",
            ]
        ):
            return False
        if modification["severity"] not in ["low", "medium", "high", "critical"]:
            return False

    for insertion in pred.insertions:
        if not isinstance(insertion, dict) or not all(
            k in insertion
            for k in [
                "line_number",
                "suggested_content",
                "reason",
                "section",
                "severity",
            ]
        ):
            return False
        if insertion["severity"] not in ["low", "medium", "high", "critical"]:
            return False

    return True


# Example training data - REPLACE WITH YOUR HIGH-QUALITY EXAMPLES
trainset = [
    dspy.Example(
        article_text="""The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet. 
        However, it has some issues that need to be addressed for better clarity and flow.""",
        score=75,
        total_issues=3,
        summary="The article conveys basic information but has several issues with redundancy, specificity, and flow that could be improved.",
        deletions=[
            {
                "line_number": 1,
                "content": "However,",
                "reason": "The word 'However' creates an unnecessary contrast when no prior statement was made",
                "severity": "low",
            },
            {
                "line_number": 2,
                "content": "that need to be addressed for better clarity and flow",
                "reason": "This phrase is vague and adds wordiness without specific value",
                "severity": "medium",
            },
        ],
        modifications=[
            {
                "line_number": 1,
                "original_content": "The quick brown fox jumps over the lazy dog.",
                "suggested_modification": "A quick brown fox jumps over a lazy dog.",
                "reason": "Using indefinite articles makes the sentence more generic and appropriate for an example",
                "severity": "low",
            }
        ],
        insertions=[
            {
                "line_number": 2,
                "suggested_content": "Specifically, the sentence could benefit from more precise vocabulary and varied sentence structure to enhance readability.",
                "reason": "Adding specific guidance on how to improve the sentence provides actionable feedback to the author",
                "section": "Feedback",
                "severity": "medium",
            }
        ],
        proofreading_rules_applied=["Grammar", "Clarity", "Conciseness", "Style"],
    ).with_inputs("article_text"),
    # Add more examples as needed - aim for 5-10 high-quality examples
]

# Optimize using BootstrapFewShot (good starting point)

print("Optimizing ArticleReviewModel with Ollama...")
optimizer = BootstrapFewShot(
    metric=article_review_metric, max_bootstrapped_demos=3, max_labeled_demos=5
)

optimized_article_review = optimizer.compile(ArticleReviewModel, trainset=trainset)

print("Optimization complete!")

# Test the optimized model
test_article = """Machine learning is a subset of artificial intelligence. It enables systems to learn from data. 
Many companies use machine learning for various applications."""

try:
    result = optimized_article_review(article_text=test_article)
    print("\n=== Test Result ===")
    print(f"Score: {result.score}")
    print(f"Summary: {result.summary}")
    print(f"Total Issues: {result.total_issues}")
    print(f"Number of Deletions: {len(result.deletions)}")
    print(f"Number of Modifications: {len(result.modifications)}")
    print(f"Number of Insertions: {len(result.insertions)}")
except Exception as e:
    print(f"Error during prediction: {e}")

# Optional: Save the optimized model for later use
# import pickle
# with open('optimized_article_review_model.pkl', 'wb') as f:
#     pickle.dump(optimized_article_review, f)


from typing import Any

class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
