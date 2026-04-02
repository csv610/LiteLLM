"""
article_reviewer_agents.py - LiteClient-only multi-stage article reviewer.
"""

import asyncio
import json
from typing import List

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

from .article_reviewer_models import (
    ArticleReviewModel,
    DeleteModel,
    InsertModel,
    ModifyModel,
)
from ..nonagentic.article_reviewer_prompts import PromptBuilder


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
