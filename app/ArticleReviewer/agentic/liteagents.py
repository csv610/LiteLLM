"""
liteagents.py - Unified LiteClient-based agents for ArticleReviewer.
"""

from ..nonagentic.article_reviewer_prompts import PromptBuilder
from app.ArticleReviewer.shared.models import (
from app.ArticleReviewer.shared.models import *
from app.ArticleReviewer.shared.models import ModelOutput
from app.ArticleReviewer.shared.utils import (
from app.ArticleReviewer.shared.utils import *
from article_reviewer_models import (
from dspy.teleprompt import BootstrapFewShot
from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from typing import Any
from typing import List
import asyncio
import dspy
import json

"""
article_reviewer_agents.py - LiteClient-only multi-stage article reviewer.
"""

    ArticleReviewModel,
    DeleteModel,
    InsertModel,
    ModifyModel,
    ModelOutput,
)

def _parse_model_response(response, response_model):
    """Normalize LiteClient responses into a target Pydantic model."""
    if isinstance(response, response_model):
        return response
    if hasattr(response, "model_dump"):
        return response_model(**response.model_dump())
    if isinstance(response, str):
        return response_model(**json.loads(response))
    if hasattr(response, "data"):
        data = response.data
        if isinstance(data, response_model):
            return data
        if isinstance(data, dict):
            return response_model(**data)
    raise ValueError(
        f"Expected {response_model.__name__} or JSON string, got {type(response).__name__}"
    )

class DeletionsResponseModel(ArticleReviewModel):
    """Structured response for deletion-only review passes."""

    deletions: List[DeleteModel] = []
    modifications: List[ModifyModel] = []
    insertions: List[InsertModel] = []

class ModificationsResponseModel(ArticleReviewModel):
    """Structured response for modification-only review passes."""

    deletions: List[DeleteModel] = []
    modifications: List[ModifyModel] = []
    insertions: List[InsertModel] = []

class InsertionsResponseModel(ArticleReviewModel):
    """Structured response for insertion-only review passes."""

    deletions: List[DeleteModel] = []
    modifications: List[ModifyModel] = []
    insertions: List[InsertModel] = []

class MultiAgentReviewer:
    """Orchestrator for the LiteClient-based multi-stage article reviewer."""

    def __init__(self, model_config: ModelConfig = None):
        if model_config is None:
            model_config = ModelConfig(model="ollama/gemma3", temperature=0.3)

        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)

    def _build_specialist_prompt(self, article_text: str, focus: str) -> str:
        base_prompt = PromptBuilder.create_review_prompt(article_text)
        return (
            f"{base_prompt}\n\n"
            "SPECIALIST MODE:\n"
            f"You are responsible only for {focus}.\n"
            "Return substantive findings for your area and leave the other categories empty.\n"
            "Keep the score and summary consistent with your specialist pass."
        )

    def _run_specialist(self, article_text: str, focus: str, response_model):
        model_input = ModelInput(
            user_prompt=self._build_specialist_prompt(article_text, focus),
            response_format=response_model,
        )
        response = self.client.generate_text(model_input=model_input)
        return _parse_model_response(response, response_model)

    def _run_manager(
        self,
        article_text: str,
        deletions: List[DeleteModel],
        modifications: List[ModifyModel],
        insertions: List[InsertModel],
        proofreading_rules_applied: List[str],
    ) -> str:
        manager_prompt = f"""
You are the lead article reviewer. Synthesize specialist feedback into one final report in Markdown format.

ARTICLE TO REVIEW:
<article>
{article_text}
</article>

SPECIALIST FEEDBACK:
{json.dumps({
    "deletions": [item.model_dump() for item in deletions],
    "modifications": [item.model_dump() for item in modifications],
    "insertions": [item.model_dump() for item in insertions],
    "proofreading_rules_applied": proofreading_rules_applied,
}, indent=2)}

INSTRUCTIONS:
1. Merge the specialist findings without inventing contradictory edits.
2. Remove duplicates if multiple specialists imply the same issue.
3. Provide one overall score from 0-100 prominently.
4. Provide a concise summary of overall article quality.
5. List all retained deletions, modifications, and insertions in a well-formatted Markdown structure.
6. Use headers, bullet points, and bold text for readability.
"""
        model_input = ModelInput(
            user_prompt=manager_prompt,
            response_format=None, # Markdown output
        )
        return self.client.generate_text(model_input=model_input)

    async def review(self, article_text: str) -> ModelOutput:
        """Review an article using LiteClient-only multi-stage orchestration."""
        deletions_task = asyncio.to_thread(
            self._run_specialist,
            article_text,
            "deletions",
            DeletionsResponseModel,
        )
        modifications_task = asyncio.to_thread(
            self._run_specialist,
            article_text,
            "modifications",
            ModificationsResponseModel,
        )
        insertions_task = asyncio.to_thread(
            self._run_specialist,
            article_text,
            "insertions",
            InsertionsResponseModel,
        )

        deletions_response, modifications_response, insertions_response = await asyncio.gather(
            deletions_task,
            modifications_task,
            insertions_task,
        )

        deletions = [
            item for item in deletions_response.deletions if item.content.strip() != ""
        ]
        modifications = modifications_response.modifications
        insertions = insertions_response.insertions

        proofreading_rules_applied = list(
            dict.fromkeys(
                deletions_response.proofreading_rules_applied
                + modifications_response.proofreading_rules_applied
                + insertions_response.proofreading_rules_applied
            )
        )

        final_markdown = await asyncio.to_thread(
            self._run_manager,
            article_text,
            deletions,
            modifications,
            insertions,
            proofreading_rules_applied,
        )

        # Create intermediate data for the .data member
        # (This preserves the structured facts from Tier 1)
        review_data = ArticleReviewModel(
            score=0, # The manager's markdown has the score now, 
                     # but we can extract it or leave as 0 if not critical for .data here
            summary="Synthesized review",
            total_issues=len(deletions) + len(modifications) + len(insertions),
            deletions=deletions,
            modifications=modifications,
            insertions=insertions,
            proofreading_rules_applied=proofreading_rules_applied
        )

        return ModelOutput(
            data=review_data,
            markdown=final_markdown,
            metadata={"process": "3-tier specialist-auditor-synthesis"}
        )

if __name__ == "__main__":
    async def test():
        reviewer = MultiAgentReviewer()
        article = "This is a test article. It is redundant. It is redundant."
        try:
            review = await reviewer.review(article)
            print("Review successful!")
            print(f"Score: {review.score}")
            print(f"Issues: {review.total_issues}")
        except Exception as exc:
            print(f"Review failed: {exc}")

    asyncio.run(test())

"""
article_reviewer_utils.py - Utility functions for article reviewer
"""

    save_review as _save_review,
    print_review as _print_review
)

def save_review(output: ModelOutput, output_filename: str = None, input_filename: str = None, output_dir: str = "outputs") -> str:
    """Save the review artifact to files (.md and .json). delegates to shared.utils."""
    return _save_review(output, output_filename, input_filename, output_dir)

def print_review(output: ModelOutput) -> None:
    """Print the synthesized Markdown review to the console. delegates to shared.utils."""
    _print_review(output)

    DeleteModel,
    ModifyModel,
    InsertModel,
    ArticleReviewModel,
    ModelOutput
)

"""
optimize_models.py - Script to optimize Pydantic models for ArticleReviewer using DSPydantic with Ollama.
"""

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

class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)

