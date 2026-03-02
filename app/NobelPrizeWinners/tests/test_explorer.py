import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Mock the lite package before importing NobelPrizeWinnerInfo
mock_lite = MagicMock()
sys.modules["lite"] = mock_lite
sys.modules["lite.lite_client"] = MagicMock()
sys.modules["lite.config"] = MagicMock()
sys.modules["lite.logging_config"] = MagicMock()

from nobel_prize_explorer import NobelPrizeWinnerInfo
from nobel_prize_models import PrizeWinner, PrizeResponse

@pytest.fixture
def mock_model_config():
    config = MagicMock()
    config.model = "test-model"
    return config

def test_validate_model_name():
    explorer = NobelPrizeWinnerInfo(MagicMock())
    # Should not raise
    explorer._validate_model_name("gpt-4")
    explorer._validate_model_name("gemini/gemini-1.5-pro")
    
    # Should raise
    with pytest.raises(ValueError):
        explorer._validate_model_name("invalid model!")

@patch("nobel_prize_explorer.LiteClient")
def test_fetch_winners(mock_client_class, mock_model_config):
    mock_client = mock_client_class.return_value
    
    # Mock response
    mock_winner = MagicMock(spec=PrizeWinner)
    mock_winner.name = "Test Winner"
    mock_response = MagicMock(spec=PrizeResponse)
    mock_response.winners = [mock_winner]
    
    mock_client.generate_text.return_value = mock_response
    
    explorer = NobelPrizeWinnerInfo(mock_model_config)
    winners = explorer.fetch_winners("Physics", "2020")
    
    assert len(winners) == 1
    assert winners[0].name == "Test Winner"
    mock_client.generate_text.assert_called_once()
