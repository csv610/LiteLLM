import pytest
from unittest.mock import patch, MagicMock
import json

from UnsolvedProblems.nonagentic.unsolved_problems import UnsolvedProblemsGuide
from UnsolvedProblems.nonagentic.unsolved_problems_models import UnsolvedProblemModel, ProblemStatus

@pytest.fixture
def mock_lite_client():
    with patch('UnsolvedProblems.nonagentic.unsolved_problems.LiteClient') as mock:
        yield mock

def test_generate_text_nonagentic(mock_lite_client):
    sample = UnsolvedProblemModel(
        title="P vs NP",
        category="Computer Science",
        description="Can every problem whose solution can be quickly verified by a computer also be quickly solved by a computer?",
        status=ProblemStatus.UNSOLVED,
        importance="Fundamental",
        related_fields=["Complexity Theory"]
    )
    instance = mock_lite_client.return_value
    instance.generate_text.return_value = sample
    
    guide = UnsolvedProblemsGuide()
    result = guide.generate_text("P vs NP")
    
    assert result.title == "P vs NP"
    assert instance.generate_text.call_count == 1
