from unittest.mock import MagicMock, patch
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "agentic"))

from . import nobel_prize_info


def test_fetch_nobel_winners_uses_resolved_model_from_environment(monkeypatch):
    monkeypatch.setenv("NOBEL_PRIZE_MODEL", "env-model")

    mock_explorer = MagicMock()
    mock_explorer.fetch_winners.return_value = ["winner"]

    with patch.object(nobel_prize_info, "NobelPrizeWinnerInfo", return_value=mock_explorer) as mock_explorer_cls:
        winners = nobel_prize_info.fetch_nobel_winners("Physics", "2023")

    assert winners == ["winner"]
    assert mock_explorer_cls.call_args.args[0].model == "env-model"
    mock_explorer.fetch_winners.assert_called_once_with("Physics", "2023", "env-model")


def test_fetch_nobel_winners_prefers_explicit_model():
    mock_explorer = MagicMock()
    mock_explorer.fetch_winners.return_value = ["winner"]

    with patch.object(nobel_prize_info, "NobelPrizeWinnerInfo", return_value=mock_explorer) as mock_explorer_cls:
        winners = nobel_prize_info.fetch_nobel_winners("Physics", "2023", model="explicit-model")

    assert winners == ["winner"]
    assert mock_explorer_cls.call_args.args[0].model == "explicit-model"
    mock_explorer.fetch_winners.assert_called_once_with("Physics", "2023", "explicit-model")
