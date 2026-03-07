import json
from unittest.mock import MagicMock, patch

import pytest

from medkit_agent.orchestrator import MedKitOrchestrator


class TestMedKitOrchestrator:
    """Tests for the MedKit Agentic Orchestrator."""

    @pytest.fixture
    def orchestrator(self):
        """Provide a MedKitOrchestrator instance for testing."""
        return MedKitOrchestrator(model="test-model", max_steps=2)

    def test_orchestrator_initialization(self, orchestrator):
        """Test basic initialization of the orchestrator."""
        assert orchestrator.model == "test-model"
        assert orchestrator.max_steps == 2
        assert len(orchestrator.tools) > 0
        assert "get_medicine_info" in [t["name"] for t in orchestrator.tools]

    @patch("medkit_agent.orchestrator.explain_medicine")
    def test_call_tool_get_medicine_info(self, mock_explain, orchestrator):
        """Test calling the get_medicine_info tool."""
        mock_explain.return_value = "Mocked explanation"

        args = {"medicine_name": "Aspirin"}
        output = orchestrator.call_tool("get_medicine_info", args)

        assert output.tool_name == "get_medicine_info"
        assert output.result == "Mocked explanation"
        mock_explain.assert_called_once_with("Aspirin")

    @patch("medkit_agent.orchestrator.completion")
    def test_run_direct_answer(self, mock_completion, orchestrator):
        """Test the run method when the agent provides a direct answer."""
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message={"content": "Direct answer", "role": "assistant"})
        ]
        mock_completion.return_value = mock_response

        result = orchestrator.run("What is health?")

        assert result == "Direct answer"
        assert len(orchestrator.history) == 1
        assert orchestrator.history[0]["content"] == "What is health?"

    @patch("medkit_agent.orchestrator.completion")
    @patch("medkit_agent.orchestrator.explain_medicine")
    def test_run_with_tool_call(self, mock_explain, mock_completion, orchestrator):
        """Test the reasoning loop when a tool call is required."""
        # 1. First call returns a tool call
        tool_call_msg = {
            "role": "assistant",
            "content": "I'll check the medicine info.",
            "function_call": {
                "name": "get_medicine_info",
                "arguments": json.dumps({"medicine_name": "Aspirin"}),
            },
        }

        # 2. Second call returns the final synthesis
        final_msg = {"role": "assistant", "content": "Aspirin is for pain."}

        mock_resp_1 = MagicMock()
        mock_resp_1.choices = [MagicMock(message=tool_call_msg)]

        mock_resp_2 = MagicMock()
        mock_resp_2.choices = [MagicMock(message=final_msg)]

        mock_completion.side_effect = [mock_resp_1, mock_resp_2]
        mock_explain.return_value = "Aspirin data"

        result = orchestrator.run("Tell me about Aspirin")

        assert result == "Aspirin is for pain."
        assert mock_explain.called
        assert len(orchestrator.history) >= 2  # Question + Tool call + Result
