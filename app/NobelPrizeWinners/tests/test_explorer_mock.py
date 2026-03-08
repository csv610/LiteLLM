import pytest
from unittest.mock import MagicMock, patch
import sys

# Mock the lite package dependencies before they are imported by nobel_prize_explorer
sys.modules["lite"] = MagicMock()
sys.modules["lite.lite_client"] = MagicMock()
sys.modules["lite.config"] = MagicMock()
sys.modules["lite.logging_config"] = MagicMock()

# Now we can import it
import nobel_prize_explorer
from nobel_prize_models import PrizeWinner, PrizeResponse

@pytest.fixture
def mock_explorer():
    with patch("nobel_prize_explorer.LiteClient"), \
         patch("nobel_prize_explorer.logging_config") as mock_log:
        mock_log.setup_logging.return_value = MagicMock()
        model_config = MagicMock()
        model_config.model = "test-model"
        explorer = nobel_prize_explorer.NobelPrizeWinnerInfo(model_config)
        yield explorer

def test_validate_model_name(mock_explorer):
    # Should not raise
    mock_explorer._validate_model_name("gpt-4")
    mock_explorer._validate_model_name("gemini/gemini-1.5-pro")
    
    # Should raise
    with pytest.raises(ValueError):
        mock_explorer._validate_model_name("invalid model!")

def test_fetch_winners(mock_explorer):
    mock_client = mock_explorer.client
    
    # Mock response
    mock_winner = MagicMock(spec=PrizeWinner)
    mock_winner.name = "Test Winner"
    mock_response = MagicMock(spec=PrizeResponse)
    mock_response.winners = [mock_winner]
    
    mock_client.generate_text.return_value = mock_response
    
    winners = mock_explorer.fetch_winners("Physics", "2020")
    
    assert len(winners) == 1
    assert winners[0].name == "Test Winner"
    mock_client.generate_text.assert_called_once()
