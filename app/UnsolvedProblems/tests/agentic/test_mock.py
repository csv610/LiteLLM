import pytest
from unittest.mock import patch, MagicMock
import json

from UnsolvedProblems.agentic.unsolved_problems import UnsolvedProblemsGuide
from UnsolvedProblems.agentic.unsolved_problems_models import UnsolvedProblemModel, ProblemStatus

@pytest.fixture
def mock_lite_client():
    with patch('UnsolvedProblems.agentic.unsolved_problems.LiteClient') as mock:
        yield mock

def test_generate_text_agentic(mock_lite_client):
    sample = UnsolvedProblemModel(
        title="P vs NP",
        category="Computer Science",
        description="P vs NP problem.",
        status=ProblemStatus.UNSOLVED,
        importance="Fundamental",
        related_fields=["Complexity Theory"]
    )
    instance = mock_lite_client.return_value
    # Researcher + Reviewer
    instance.generate_text.side_effect = [sample, sample]
    
    guide = UnsolvedProblemsGuide()
    result = guide.generate_text("P vs NP")
    
    assert result.title == "P vs NP"
    assert instance.generate_text.call_count == 2
