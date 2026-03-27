import pytest
import argparse
from datetime import datetime
from pathlib import Path
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "agentic"))

import nobel_prize_cli
from nobel_prize_cli import validate_year, validate_category

def test_validate_year_valid():
    assert validate_year("1901") == 1901
    assert validate_year(str(datetime.now().year)) == datetime.now().year

def test_validate_year_invalid():
    with pytest.raises(argparse.ArgumentTypeError):
        validate_year("1900")
    with pytest.raises(argparse.ArgumentTypeError):
        validate_year(str(datetime.now().year + 1))
    with pytest.raises(argparse.ArgumentTypeError):
        validate_year("abc")

def test_validate_category_valid():
    assert validate_category("Physics") == "Physics"
    assert validate_category("physics") == "Physics"
    assert validate_category("CHEMISTRY") == "Chemistry"
    assert validate_category("Medicine") == "Medicine"
    assert validate_category("Literature") == "Literature"
    assert validate_category("Peace") == "Peace"
    assert validate_category("Economics") == "Economics"

def test_validate_category_invalid():
    with pytest.raises(argparse.ArgumentTypeError):
        validate_category("Math")
    with pytest.raises(argparse.ArgumentTypeError):
        validate_category("Invalid")

def test_main_returns_error_when_logger_setup_fails(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["nobel_prize_cli.py", "-c", "Physics", "-y", "2023"])

    with patch.object(nobel_prize_cli.logging_config, "configure_logging", side_effect=RuntimeError("log setup failed")):
        exit_code = nobel_prize_cli.main()

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "log setup failed" in captured.out

def test_main_resolves_model_before_fetch(monkeypatch):
    monkeypatch.setattr("sys.argv", ["nobel_prize_cli.py", "-c", "Physics", "-y", "2023"])
    monkeypatch.setenv("NOBEL_PRIZE_MODEL", "env-model")

    mock_logger = MagicMock()
    mock_winner = MagicMock()
    mock_winner.model_dump.return_value = {"name": "Winner"}
    mock_winner.name = "Winner"
    mock_winner.year = 2023

    with patch.object(nobel_prize_cli.logging_config, "configure_logging", return_value=mock_logger), \
         patch.object(nobel_prize_cli, "fetch_nobel_winners", return_value=[mock_winner]) as mock_fetch, \
         patch.object(nobel_prize_cli.json, "dump"), \
         patch.object(nobel_prize_cli.os, "chmod"):
        exit_code = nobel_prize_cli.main()

    assert exit_code == 0
    mock_fetch.assert_called_once_with("Physics", "2023", model="env-model")
