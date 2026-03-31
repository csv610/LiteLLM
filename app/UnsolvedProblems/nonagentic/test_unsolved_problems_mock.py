import pytest
from unittest.mock import patch, MagicMock
import json

from UnsolvedProblems.nonagentic.unsolved_problems_explorer import (
    UnsolvedProblemsExplorer,
)
from UnsolvedProblems.nonagentic.unsolved_problems_models import UnsolvedProblem
from lite.lite_client import ModelConfig


@pytest.fixture
def mock_lite_client():
    with patch(
        "UnsolvedProblems.nonagentic.unsolved_problems_explorer.LiteClient"
    ) as mock:
        yield mock


def test_generate_text_nonagentic(mock_lite_client):
    sample = UnsolvedProblem(
        title="P vs NP",
        description="Can every problem whose solution can be quickly verified by a computer also be quickly solved by a computer?",
        field="Computer Science",
        difficulty="Advanced",
        first_posed="1971 by Stephen Cook",
        prize_money="$1,000,000 Clay Millennium Prize",
        significance="Fundamental to understanding the limits of computation",
        current_status="P vs NP remains unsolved despite extensive research",
    )
    instance = mock_lite_client.return_value
    instance.generate_text.return_value = sample

    mock_config = ModelConfig(model="test-model", temperature=0.2)
    guide = UnsolvedProblemsExplorer(mock_config)
    result = guide.generate_text("P vs NP", 1)

    assert result.title == "P vs NP"
    assert instance.generate_text.call_count == 1
