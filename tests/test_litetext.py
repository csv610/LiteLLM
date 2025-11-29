"""Tests for LiteText module."""

import pytest
from unittest.mock import patch, MagicMock

from lite.litellm_tools import ModelConfig, LiteText, LiteTextResponse


class TestModelConfig:
    """Test ModelConfig class."""

    def test_get_model_valid_index_text(self):
        """Test getting a text model with valid index."""
        model = ModelConfig.get_model(0, "text")
        assert model == "openai/gpt-4o"

    def test_get_model_valid_index_vision(self):
        """Test getting a vision model with valid index."""
        model = ModelConfig.get_model(0, "vision")
        assert model == "openai/gpt-4o"

    def test_get_model_invalid_negative_index(self):
        """Test getting a model with negative index."""
        model = ModelConfig.get_model(-1, "text")
        assert model is None

    def test_get_model_invalid_out_of_range(self):
        """Test getting a model with index out of range."""
        model = ModelConfig.get_model(999, "text")
        assert model is None

    def test_text_models_list_not_empty(self):
        """Test that text models list is populated."""
        assert len(ModelConfig.TEXT_MODELS) > 0

    def test_vision_models_list_not_empty(self):
        """Test that vision models list is populated."""
        assert len(ModelConfig.VISION_MODELS) > 0

    def test_get_models_text(self):
        """Test getting all text models."""
        models = ModelConfig.get_models("text")
        assert len(models) > 0
        assert all(isinstance(m, str) for m in models)

    def test_get_models_vision(self):
        """Test getting all vision models."""
        models = ModelConfig.get_models("vision")
        assert len(models) > 0
        assert all(isinstance(m, str) for m in models)


class TestLiteTextResponse:
    """Test LiteTextResponse class."""

    def test_response_success(self):
        """Test successful response."""
        response = LiteTextResponse(
            response="Hello", response_time=1.5, word_count=1
        )
        assert response.is_success() is True
        assert response.response == "Hello"
        assert response.error is None

    def test_response_error(self):
        """Test error response."""
        response = LiteTextResponse(error="API Error")
        assert response.is_success() is False
        assert response.error == "API Error"
        assert response.response is None

    def test_response_default_values(self):
        """Test default values in response."""
        response = LiteTextResponse()
        assert response.response is None
        assert response.response_time == 0.0
        assert response.word_count == 0
        assert response.error is None


class TestLiteText:
    """Test LiteText class."""

    def test_get_response_empty_prompt(self):
        """Test that empty prompt returns error."""
        response = LiteText.get_response("", "openai/gpt-4o")
        assert response.is_success() is False
        assert "Prompt cannot be empty" in response.error

    def test_get_response_whitespace_only_prompt(self):
        """Test that whitespace-only prompt returns error."""
        response = LiteText.get_response("   ", "openai/gpt-4o")
        assert response.is_success() is False

    @patch("lite.litellm_tools.text.completion")
    def test_get_response_success(self, mock_completion):
        """Test successful API response."""
        # Mock the completion response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "This is a test response"
        mock_completion.return_value = mock_response

        response = LiteText.get_response("Test prompt", "openai/gpt-4o")

        assert response.is_success() is True
        assert response.response == "This is a test response"
        assert response.word_count == 5
        assert response.response_time > 0

    @patch("lite.litellm_tools.text.completion")
    def test_get_response_with_custom_params(self, mock_completion):
        """Test API response with custom temperature and max_tokens."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Response"
        mock_completion.return_value = mock_response

        LiteText.get_response(
            "Test", "openai/gpt-4o", temperature=0.5, max_tokens=500
        )

        # Verify the API was called with correct parameters
        mock_completion.assert_called_once()
        call_kwargs = mock_completion.call_args[1]
        assert call_kwargs["temperature"] == 0.5
        assert call_kwargs["max_tokens"] == 500

    @patch("lite.litellm_tools.text.completion")
    def test_get_response_api_error(self, mock_completion):
        """Test handling of API error."""
        from litellm import APIError

        mock_completion.side_effect = APIError("API connection failed")

        response = LiteText.get_response("Test", "openai/gpt-4o")

        assert response.is_success() is False
        assert "API Error" in response.error

    @patch("lite.litellm_tools.text.completion")
    def test_get_response_unexpected_error(self, mock_completion):
        """Test handling of unexpected error."""
        mock_completion.side_effect = ValueError("Unexpected error")

        response = LiteText.get_response("Test", "openai/gpt-4o")

        assert response.is_success() is False
        assert "Unexpected error" in response.error

    @patch("lite.litellm_tools.text.completion")
    def test_word_count(self, mock_completion):
        """Test word count calculation."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "One two three four five"
        mock_completion.return_value = mock_response

        response = LiteText.get_response("Test", "openai/gpt-4o")
        assert response.word_count == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
