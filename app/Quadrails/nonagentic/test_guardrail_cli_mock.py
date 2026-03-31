import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import sys
import os

from .guardrail_cli import main, argument_parser


def test_argument_parser():
    parser = argument_parser()

    # Test text input
    args = parser.parse_args(["-t", "Hello world"])
    assert args.text == "Hello world"

    # Test image input
    args = parser.parse_args(["-i", "test.jpg"])
    assert args.image == "test.jpg"

    # Test model
    args = parser.parse_args(["-m", "ollama/mistral"])
    assert args.model == "ollama/mistral"

    # Test no-cache
    args = parser.parse_args(["-t", "hi", "--no-cache"])
    assert args.no_cache is True


def test_argument_parser_env_default():
    with patch.dict(os.environ, {"GUARDRAIL_MODEL": "ollama/test-model"}):
        parser = argument_parser()
        args = parser.parse_args(["-t", "hi"])
        assert args.model == "ollama/test-model"


@patch("Quadrails.nonagentic.guardrail_cli.GuardrailAnalyzer")
def test_main_with_no_cache(mock_analyzer_class, capsys):
    mock_analyzer = mock_analyzer_class.return_value
    mock_result = MagicMock()
    mock_analyzer.analyze_text = AsyncMock(return_value=mock_result)

    with patch.object(
        sys, "argv", ["guardrail_cli.py", "-t", "some text", "--no-cache"]
    ):
        main()

    mock_analyzer.analyze_text.assert_called_with("some text", use_cache=False)


@patch("Quadrails.nonagentic.guardrail_cli.GuardrailAnalyzer")
def test_main_with_image(mock_analyzer_class, capsys):
    mock_analyzer = mock_analyzer_class.return_value
    mock_result = MagicMock()
    mock_analyzer.analyze_image = AsyncMock(return_value=mock_result)

    with patch.object(sys, "argv", ["guardrail_cli.py", "-i", "test.jpg"]):
        main()

    mock_analyzer.analyze_image.assert_called_with("test.jpg", use_cache=True)
    mock_analyzer_class.display_results.assert_called_once()


@patch("Quadrails.nonagentic.guardrail_cli.GuardrailAnalyzer")
def test_main_no_input(mock_analyzer_class, capsys):
    with patch.object(sys, "argv", ["guardrail_cli.py"]):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0
