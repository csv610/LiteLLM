import json
import pytest
from unittest.mock import patch, MagicMock
import asyncio

from ArticleReviewer.agentic.article_reviewer_agents import LiteModel, MultiAgentReviewer
from ArticleReviewer.agentic.article_reviewer_models import (
    DeleteModel, ModifyModel, InsertModel, ArticleReviewModel
)
from lite.config import ModelConfig

# Test LiteModel
@pytest.mark.anyio
async def test_lite_model_request():
    model_config = ModelConfig(model="gpt-4")
    lite_model = LiteModel(model_config)
    
    with patch('ArticleReviewer.agentic.article_reviewer_agents.LiteClient') as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.generate_text.return_value = '{"score": 90, "total_issues": 0, "summary": "Great", "deletions": [], "modifications": [], "insertions": [], "proofreading_rules_applied": []}'
        
        # Mocking ModelMessage and RunContext is complex, so let's mock LiteClient directly
        # and test how it is called through LiteModel.request
        
        from pydantic_ai.messages import ModelRequest, TextPart
        from pydantic_ai.models import ModelRequestParameters
        
        messages = [ModelRequest(parts=[TextPart(content="Test content")])]
        model_request_parameters = MagicMock(spec=ModelRequestParameters)
        model_request_parameters.output_object = None
        
        response = await lite_model.request(messages, None, model_request_parameters)
        
        assert response.model_name == "gpt-4"
        assert "Great" in response.parts[0].content

# Test MultiAgentReviewer
@pytest.fixture
def mock_lite_model():
    with patch('ArticleReviewer.agentic.article_reviewer_agents.LiteModel') as mock:
        yield mock

@pytest.mark.anyio
async def test_multi_agent_reviewer_init(mock_lite_model):
    reviewer = MultiAgentReviewer()
    assert reviewer.model is not None
    assert reviewer.deletions_agent is not None
    assert reviewer.modifications_agent is not None
    assert reviewer.insertions_agent is not None
    assert reviewer.manager_agent is not None

@pytest.mark.anyio
async def test_multi_agent_reviewer_review(mock_lite_model):
    # Mocking the agents to return expected outputs
    reviewer = MultiAgentReviewer()
    
    # Mocking the manager agent run result
    mock_result = MagicMock()
    mock_result.output = ArticleReviewModel(
        score=95,
        total_issues=1,
        summary="Excellent work.",
        deletions=[DeleteModel(line_number=1, content="Extra", reason="Redundant", severity="low")],
        modifications=[],
        insertions=[],
        proofreading_rules_applied=["Style"]
    )
    
    from unittest.mock import AsyncMock
    reviewer.manager_agent.run = AsyncMock(return_value=mock_result)
    
    review = await reviewer.review("Some article text")
    
    assert isinstance(review, ArticleReviewModel)
    assert review.score == 95
    assert len(review.deletions) == 1
    assert review.total_issues == 1
