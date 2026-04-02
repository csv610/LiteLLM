import pytest
from unittest.mock import patch

from app.ArticleReviewer.agentic.article_reviewer_agents import MultiAgentReviewer
from app.ArticleReviewer.agentic.article_reviewer_models import (
    ArticleReviewModel,
    DeleteModel,
)
from lite.config import ModelConfig


def test_multi_agent_reviewer_init():
    reviewer = MultiAgentReviewer()
    assert reviewer.client is not None


@pytest.mark.anyio
async def test_multi_agent_reviewer_review():
    specialist_deletions = ArticleReviewModel(
        score=82,
        total_issues=1,
        summary="Deletion pass",
        deletions=[
            DeleteModel(
                line_number=1,
                content="Extra",
                reason="Redundant",
                severity="low",
            )
        ],
        modifications=[],
        insertions=[],
        proofreading_rules_applied=["Style & Clarity"],
    )
    specialist_modifications = ArticleReviewModel(
        score=84,
        total_issues=0,
        summary="Modification pass",
        deletions=[],
        modifications=[],
        insertions=[],
        proofreading_rules_applied=["Grammar & Syntax"],
    )
    specialist_insertions = ArticleReviewModel(
        score=86,
        total_issues=0,
        summary="Insertion pass",
        deletions=[],
        modifications=[],
        insertions=[],
        proofreading_rules_applied=["Content & Structure"],
    )
    final_markdown = "# Final Review\nScore: 95\nExcellent work."

    with patch(
        "app.ArticleReviewer.agentic.article_reviewer_agents.LiteClient.generate_text",
        side_effect=[
            specialist_deletions,
            specialist_modifications,
            specialist_insertions,
            final_markdown,
        ],
    ) as mock_generate:
        reviewer = MultiAgentReviewer(ModelConfig(model="gpt-4"))
        review = await reviewer.review("Some article text")

    from app.ArticleReviewer.shared.models import ModelOutput
    assert isinstance(review, ModelOutput)
    assert review.markdown == final_markdown
    assert review.data.total_issues == 1
    assert mock_generate.call_count == 4
