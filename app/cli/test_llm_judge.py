"""
Unit and integration tests for llm_judge.py
"""

import json
import pytest
from datetime import datetime
from unittest.mock import Mock, MagicMock, patch
from llm_judge import (
    LLMJudge, JudgeConfig, JudgmentResult, ComparisonResult,
    JudgingCriteria, GeminiLLMJudge
)


class TestJudgingCriteria:
    """Test JudgingCriteria enum."""

    def test_all_criteria_present(self):
        """Test that all expected criteria are defined."""
        criteria_values = [c.value for c in JudgingCriteria]
        expected = [
            "helpfulness", "accuracy", "relevance", "safety", "clarity",
            "completeness", "coherence", "factual_correctness", "bias_detection", "toxicity"
        ]
        assert criteria_values == expected

    def test_criteria_are_strings(self):
        """Test that all criteria are string enums."""
        for criteria in JudgingCriteria:
            assert isinstance(criteria.value, str)


class TestJudgeConfig:
    """Test JudgeConfig model."""

    def test_default_config(self):
        """Test config with default values."""
        config = JudgeConfig()
        assert config.model == "gemini/gemini-2.5-flash"
        assert config.temperature == 0.1

    def test_custom_config(self):
        """Test config with custom values."""
        config = JudgeConfig(model="custom/model", temperature=0.7)
        assert config.model == "custom/model"
        assert config.temperature == 0.7

    def test_temperature_bounds(self):
        """Test temperature validation."""
        with pytest.raises(ValueError):
            JudgeConfig(temperature=-0.1)

        with pytest.raises(ValueError):
            JudgeConfig(temperature=2.1)

        # Valid boundaries
        assert JudgeConfig(temperature=0.0).temperature == 0.0
        assert JudgeConfig(temperature=2.0).temperature == 2.0


class TestJudgmentResult:
    """Test JudgmentResult model."""

    def test_basic_judgment_result(self):
        """Test creating a judgment result."""
        result = JudgmentResult(
            scores={"accuracy": 0.8},
            explanations={"accuracy": "Good accuracy"}
        )
        assert result.scores == {"accuracy": 0.8}
        assert result.explanations == {"accuracy": "Good accuracy"}
        assert result.confidence is None
        assert isinstance(result.timestamp, datetime)

    def test_judgment_result_with_confidence(self):
        """Test judgment result with confidence score."""
        result = JudgmentResult(
            scores={"accuracy": 0.8},
            explanations={"accuracy": "Good"},
            confidence=0.95
        )
        assert result.confidence == 0.95

    def test_judgment_result_timestamp_auto_set(self):
        """Test that timestamp is automatically set."""
        before = datetime.now()
        result = JudgmentResult(scores={}, explanations={})
        after = datetime.now()
        assert before <= result.timestamp <= after


class TestComparisonResult:
    """Test ComparisonResult model."""

    def test_comparison_result_with_winner(self):
        """Test comparison result with a winner."""
        result = ComparisonResult(
            response1_scores={"accuracy": 0.7},
            response2_scores={"accuracy": 0.9},
            winner=1,
            explanation="Response 2 is better"
        )
        assert result.winner == 1
        assert result.response2_scores == {"accuracy": 0.9}

    def test_comparison_result_with_tie(self):
        """Test comparison result with a tie."""
        result = ComparisonResult(
            response1_scores={"accuracy": 0.8},
            response2_scores={"accuracy": 0.8},
            winner=None,
            explanation="Both responses are equally good"
        )
        assert result.winner is None

    def test_comparison_result_timestamp_auto_set(self):
        """Test that timestamp is automatically set."""
        before = datetime.now()
        result = ComparisonResult(
            response1_scores={},
            response2_scores={},
            explanation=""
        )
        after = datetime.now()
        assert before <= result.timestamp <= after


class TestLLMJudgeInit:
    """Test LLMJudge initialization."""

    @patch('llm_judge.LiteClient')
    def test_init_with_default_config(self, mock_client):
        """Test initialization with default config."""
        judge = LLMJudge(JudgeConfig())
        assert judge.config.model == "gemini/gemini-2.5-flash"
        assert judge.config.temperature == 0.1
        assert judge.logger is not None
        mock_client.assert_called_once()

    @patch('llm_judge.LiteClient')
    def test_init_with_custom_config(self, mock_client):
        """Test initialization with custom config."""
        config = JudgeConfig(model="custom/model", temperature=0.5)
        judge = LLMJudge(config)
        assert judge.config.model == "custom/model"
        assert judge.config.temperature == 0.5

    @patch('llm_judge.LiteClient')
    def test_logger_setup(self, mock_client):
        """Test that logger is properly configured."""
        judge = LLMJudge(JudgeConfig())
        assert judge.logger.name == 'LLMJudge'
        assert judge.logger.level == 20  # INFO level is 20


class TestMakeApiRequest:
    """Test _make_api_request method."""

    @patch('llm_judge.LiteClient')
    def test_make_api_request_returns_string(self, mock_client_class):
        """Test API request returns string."""
        mock_client = MagicMock()
        mock_client.generate_text.return_value = "test response"
        mock_client_class.return_value = mock_client

        judge = LLMJudge(JudgeConfig())
        result = judge._make_api_request("test prompt")

        assert result == "test response"
        mock_client.generate_text.assert_called_once()

    @patch('llm_judge.LiteClient')
    def test_make_api_request_with_error_response(self, mock_client_class):
        """Test API request with error in response."""
        mock_client = MagicMock()
        mock_client.generate_text.return_value = {"error": "API Error"}
        mock_client_class.return_value = mock_client

        judge = LLMJudge(JudgeConfig())

        with pytest.raises(Exception) as exc_info:
            judge._make_api_request("test prompt")

        assert "API Error" in str(exc_info.value)

    @patch('llm_judge.LiteClient')
    def test_make_api_request_with_response_model_dict(self, mock_client_class):
        """Test API request parsing JSON response to model."""
        mock_client = MagicMock()
        mock_client.generate_text.return_value = '{"scores": {"accuracy": 0.8}, "explanations": {"accuracy": "Good"}}'
        mock_client_class.return_value = mock_client

        judge = LLMJudge(JudgeConfig())
        result = judge._make_api_request("test prompt", response_model=JudgmentResult)

        assert isinstance(result, JudgmentResult)
        assert result.scores == {"accuracy": 0.8}

    @patch('llm_judge.LiteClient')
    def test_make_api_request_with_response_model_dict_input(self, mock_client_class):
        """Test API request with dict response and model."""
        mock_client = MagicMock()
        mock_client.generate_text.return_value = {
            "scores": {"accuracy": 0.8},
            "explanations": {"accuracy": "Good"}
        }
        mock_client_class.return_value = mock_client

        judge = LLMJudge(JudgeConfig())
        result = judge._make_api_request("test prompt", response_model=JudgmentResult)

        assert isinstance(result, JudgmentResult)
        assert result.scores == {"accuracy": 0.8}


class TestEvaluate:
    """Test evaluate method."""

    @patch('llm_judge.LiteClient')
    def test_evaluate_single_item(self, mock_client_class):
        """Test evaluating a single item."""
        mock_client = MagicMock()
        response_json = {
            "scores": {"accuracy": 0.9, "clarity": 0.8},
            "explanations": {"accuracy": "Very accurate", "clarity": "Clear"},
            "confidence": 0.95
        }
        mock_client.generate_text.return_value = json.dumps(response_json)
        mock_client_class.return_value = mock_client

        judge = LLMJudge(JudgeConfig())
        result = judge.evaluate("Test content")

        assert isinstance(result, JudgmentResult)
        assert result.scores == {"accuracy": 0.9, "clarity": 0.8}
        assert result.confidence == 0.95
        assert "Very accurate" in result.explanations.values()

    @patch('llm_judge.LiteClient')
    def test_evaluate_with_context(self, mock_client_class):
        """Test evaluation with context."""
        mock_client = MagicMock()
        mock_client.generate_text.return_value = '{"scores": {}, "explanations": {}}'
        mock_client_class.return_value = mock_client

        judge = LLMJudge(JudgeConfig())
        judge.evaluate("Test content", context="Test context")

        # Check that context is included in prompt
        call_args = mock_client.generate_text.call_args
        prompt = call_args[1]['model_input'].user_prompt
        assert "Test context" in prompt
        assert "Context:" in prompt

    @patch('llm_judge.LiteClient')
    def test_evaluate_without_context(self, mock_client_class):
        """Test evaluation without context."""
        mock_client = MagicMock()
        mock_client.generate_text.return_value = '{"scores": {}, "explanations": {}}'
        mock_client_class.return_value = mock_client

        judge = LLMJudge(JudgeConfig())
        judge.evaluate("Test content")

        call_args = mock_client.generate_text.call_args
        prompt = call_args[1]['model_input'].user_prompt
        assert "Context:" not in prompt

    @patch('llm_judge.LiteClient')
    def test_evaluate_error_handling(self, mock_client_class):
        """Test error handling in evaluate."""
        mock_client = MagicMock()
        mock_client.generate_text.side_effect = Exception("API Error")
        mock_client_class.return_value = mock_client

        judge = LLMJudge(JudgeConfig())
        result = judge.evaluate("Test content")

        assert result.scores == {}
        assert "Error" in result.explanations.get("error", "")
        assert result.confidence == 0.0

    @patch('llm_judge.LiteClient')
    def test_evaluate_malformed_json_response(self, mock_client_class):
        """Test handling of malformed JSON response."""
        mock_client = MagicMock()
        mock_client.generate_text.return_value = "Not valid JSON"
        mock_client_class.return_value = mock_client

        judge = LLMJudge(JudgeConfig())
        result = judge.evaluate("Test content")

        assert result.scores == {}
        assert result.confidence == 0.0


class TestCompare:
    """Test compare method."""

    @patch('llm_judge.LiteClient')
    def test_compare_two_responses(self, mock_client_class):
        """Test comparing two responses."""
        mock_client = MagicMock()
        response_json = {
            "response1_scores": {"accuracy": 0.7},
            "response2_scores": {"accuracy": 0.9},
            "winner": 1,
            "explanation": "Response 2 is more accurate",
            "confidence": 0.92
        }
        mock_client.generate_text.return_value = json.dumps(response_json)
        mock_client_class.return_value = mock_client

        judge = LLMJudge(JudgeConfig())
        result = judge.compare("Response 1", "Response 2")

        assert isinstance(result, ComparisonResult)
        assert result.winner == 1
        assert result.response1_scores == {"accuracy": 0.7}
        assert result.response2_scores == {"accuracy": 0.9}
        assert result.confidence == 0.92

    @patch('llm_judge.LiteClient')
    def test_compare_with_context(self, mock_client_class):
        """Test comparison with context."""
        mock_client = MagicMock()
        mock_client.generate_text.return_value = json.dumps({
            "response1_scores": {},
            "response2_scores": {},
            "explanation": "",
            "winner": None
        })
        mock_client_class.return_value = mock_client

        judge = LLMJudge(JudgeConfig())
        judge.compare("Response 1", "Response 2", context="Test context")

        call_args = mock_client.generate_text.call_args
        prompt = call_args[1]['model_input'].user_prompt
        assert "Test context" in prompt

    @patch('llm_judge.LiteClient')
    def test_compare_tie_result(self, mock_client_class):
        """Test comparison resulting in a tie."""
        mock_client = MagicMock()
        response_json = {
            "response1_scores": {"accuracy": 0.8},
            "response2_scores": {"accuracy": 0.8},
            "winner": None,
            "explanation": "Both responses are equally good"
        }
        mock_client.generate_text.return_value = json.dumps(response_json)
        mock_client_class.return_value = mock_client

        judge = LLMJudge(JudgeConfig())
        result = judge.compare("Response 1", "Response 2")

        assert result.winner is None
        assert "equally" in result.explanation.lower()

    @patch('llm_judge.LiteClient')
    def test_compare_error_handling(self, mock_client_class):
        """Test error handling in compare."""
        mock_client = MagicMock()
        mock_client.generate_text.side_effect = Exception("API Error")
        mock_client_class.return_value = mock_client

        judge = LLMJudge(JudgeConfig())
        result = judge.compare("Response 1", "Response 2")

        assert result.response1_scores == {}
        assert result.response2_scores == {}
        assert result.winner is None
        assert "Error" in result.explanation
        assert result.confidence == 0.0


class TestBackwardCompatibility:
    """Test backward compatibility features."""

    def test_gemini_llm_judge_alias(self):
        """Test that GeminiLLMJudge is an alias for LLMJudge."""
        assert GeminiLLMJudge is LLMJudge


class TestIntegration:
    """Integration tests for complete workflows."""

    @patch('llm_judge.LiteClient')
    def test_evaluate_and_compare_workflow(self, mock_client_class):
        """Test a complete workflow of evaluating and comparing."""
        mock_client = MagicMock()

        # First call for evaluate
        eval_response = {
            "scores": {"accuracy": 0.8, "clarity": 0.7},
            "explanations": {"accuracy": "Good", "clarity": "Fair"},
            "confidence": 0.9
        }

        # Second call for compare
        compare_response = {
            "response1_scores": {"accuracy": 0.8},
            "response2_scores": {"accuracy": 0.95},
            "winner": 1,
            "explanation": "Second response is more accurate",
            "confidence": 0.88
        }

        mock_client.generate_text.side_effect = [
            json.dumps(eval_response),
            json.dumps(compare_response)
        ]
        mock_client_class.return_value = mock_client

        judge = LLMJudge(JudgeConfig())

        # Evaluate
        eval_result = judge.evaluate("Test content")
        assert eval_result.scores["accuracy"] == 0.8

        # Compare
        comp_result = judge.compare("Response 1", "Response 2")
        assert comp_result.winner == 1

    @patch('llm_judge.LiteClient')
    def test_multiple_evaluations(self, mock_client_class):
        """Test performing multiple evaluations."""
        mock_client = MagicMock()
        response = '{"scores": {"accuracy": 0.8}, "explanations": {}}'
        mock_client.generate_text.return_value = response
        mock_client_class.return_value = mock_client

        judge = LLMJudge(JudgeConfig())

        results = [
            judge.evaluate(f"Content {i}")
            for i in range(3)
        ]

        assert len(results) == 3
        assert all(isinstance(r, JudgmentResult) for r in results)
        assert mock_client.generate_text.call_count == 3
