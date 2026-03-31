import pytest
from unittest.mock import patch, MagicMock
import json

from NobelPrizeWinners.agentic.nobel_prize_explorer import NobelPrizeWinnerInfo
from NobelPrizeWinners.agentic.nobel_prize_models import PrizeWinner


@pytest.fixture
def mock_lite_client():
    with patch("NobelPrizeWinners.agentic.nobel_prize_explorer.LiteClient") as mock:
        yield mock


def test_fetch_nobel_agentic(mock_lite_client):
    sample = PrizeWinner(
        year=1921,
        category="Physics",
        laureates=["Albert Einstein"],
        citation="For his services to Theoretical Physics.",
        impact="Foundation of modern physics.",
    )
    instance = mock_lite_client.return_value
    # Researcher + Reviewer
    instance.generate_text.side_effect = [sample, sample]

    from lite.lite_client import ModelConfig

    mock_config = ModelConfig(model="test-model", temperature=0.2)
    agent = NobelPrizeWinnerInfo(mock_config)
    result = agent.fetch_prize_info(1921, "Physics")

    assert result.year == 1921
    assert "Albert Einstein" in result.laureates
    assert instance.generate_text.call_count == 2
