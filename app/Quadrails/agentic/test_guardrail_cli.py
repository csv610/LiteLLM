from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from guardrail_cli import argument_parser, run_analysis


def test_argument_parser():
    parser = argument_parser()

    args = parser.parse_args(["-t", "Hello world"])
    assert args.text == "Hello world"

    args = parser.parse_args(["-i", "test.jpg"])
    assert args.image == "test.jpg"

    args = parser.parse_args(["-m", "ollama/mistral"])
    assert args.model == "ollama/mistral"

    args = parser.parse_args(["-t", "hi", "--no-cache"])
    assert args.no_cache is True


def test_argument_parser_env_default(monkeypatch):
    monkeypatch.setenv("GUARDRAIL_MODEL", "ollama/test-model")
    parser = argument_parser()
    args = parser.parse_args(["-t", "hi"])
    assert args.model == "ollama/test-model"


@pytest.mark.parametrize(
    ("argv", "agent_name", "method_name", "expected_input"),
    [
        (["-t", "some text"], "TextGuardrailAgent", "analyze_text", "some text"),
        (["-i", "test.jpg"], "ImageGuardrailAgent", "analyze_image", "test.jpg"),
    ],
)
def test_run_analysis_dispatches_to_agents(argv, agent_name, method_name, expected_input):
    parser = argument_parser()
    args = parser.parse_args(argv)

    with patch("guardrail_cli.logging_config.configure_logging"), patch("guardrail_cli.configure_module_logging"), patch(
        f"guardrail_cli.{agent_name}"
    ) as mock_agent_class, patch("guardrail_cli.GuardrailAnalyzer.display_results") as mock_display:
        mock_agent = mock_agent_class.return_value
        setattr(mock_agent, method_name, AsyncMock(return_value=MagicMock()))

        import asyncio

        asyncio.run(run_analysis(args))

        getattr(mock_agent, method_name).assert_called_once_with(expected_input, use_cache=True)
        mock_display.assert_called_once()


def test_run_analysis_no_cache_text():
    parser = argument_parser()
    args = parser.parse_args(["-t", "some text", "--no-cache"])

    with patch("guardrail_cli.logging_config.configure_logging"), patch("guardrail_cli.configure_module_logging"), patch(
        "guardrail_cli.TextGuardrailAgent"
    ) as mock_text_agent, patch("guardrail_cli.ImageGuardrailAgent"), patch(
        "guardrail_cli.GuardrailAnalyzer.display_results"
    ):
        mock_text_agent.return_value.analyze_text = AsyncMock(return_value=MagicMock())

        import asyncio

        asyncio.run(run_analysis(args))

        mock_text_agent.return_value.analyze_text.assert_called_once_with("some text", use_cache=False)
