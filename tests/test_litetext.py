"""Tests for LiteClient and ModelConfig modules."""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add lite directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lite'))

from lite_client import LiteClient
from config import ModelConfig


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


class TestLiteClient:
    """Test LiteClient class."""

    def test_create_message_text_only(self):
        """Test creating a message with text only."""
        prompt = "What is AI?"
        message = LiteClient.create_message(prompt)

        assert isinstance(message, list)
        assert len(message) == 1
        assert message[0]["role"] == "user"
        assert len(message[0]["content"]) == 1
        assert message[0]["content"][0]["type"] == "text"
        assert message[0]["content"][0]["text"] == prompt

    @patch('image_utils.ImageUtils.encode_to_base64')
    def test_create_message_with_image(self, mock_encode):
        """Test creating a message with text and image."""
        mock_encode.return_value = "data:image/jpeg;base64,fake_base64_data"

        prompt = "Describe this image"
        image_path = "/path/to/image.jpg"
        message = LiteClient.create_message(prompt, image_path)

        assert isinstance(message, list)
        assert len(message) == 1
        assert message[0]["role"] == "user"
        assert len(message[0]["content"]) == 2
        assert message[0]["content"][0]["type"] == "text"
        assert message[0]["content"][1]["type"] == "image_url"

    def test_generate_text_empty_prompt_no_image(self):
        """Test that empty prompt without image returns error."""
        client = LiteClient()
        result = client.generate_text("", "openai/gpt-4o")

        assert isinstance(result, str)
        assert "Error" in result

    def test_generate_text_whitespace_only_prompt_no_image(self):
        """Test that whitespace-only prompt without image returns error."""
        client = LiteClient()
        result = client.generate_text("   ", "openai/gpt-4o")

        assert isinstance(result, str)
        assert "Error" in result

    def test_generate_text_empty_prompt_with_image(self):
        """Test that empty prompt with image uses default prompt."""
        client = LiteClient()

        with patch('lite_client.completion') as mock_completion:
            with patch('image_utils.ImageUtils.encode_to_base64'):
                mock_response = MagicMock()
                mock_response.choices[0].message.content = "Image description"
                mock_completion.return_value = mock_response

                result = client.generate_text("", "openai/gpt-4o", image_path="/path/to/image.jpg")

                assert result == "Image description"
                # Verify that completion was called with "Describe the image"
                mock_completion.assert_called_once()

    @patch('lite_client.completion')
    def test_generate_text_success(self, mock_completion):
        """Test successful text generation."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "This is a test response"
        mock_completion.return_value = mock_response

        client = LiteClient()
        result = client.generate_text("Test prompt", "openai/gpt-4o")

        assert result == "This is a test response"
        mock_completion.assert_called_once()

    @patch('lite_client.completion')
    def test_generate_text_with_custom_temperature(self, mock_completion):
        """Test text generation with custom temperature."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Response"
        mock_completion.return_value = mock_response

        client = LiteClient()
        client.generate_text("Test", "openai/gpt-4o", temperature=0.8)

        mock_completion.assert_called_once()
        call_kwargs = mock_completion.call_args[1]
        assert call_kwargs["temperature"] == 0.8

    @patch('lite_client.completion')
    def test_generate_text_api_error(self, mock_completion):
        """Test handling of API error."""
        from litellm import APIError

        mock_completion.side_effect = APIError(
            status_code=500,
            message="API connection failed",
            llm_provider="openai",
            model="gpt-4o"
        )

        client = LiteClient()
        result = client.generate_text("Test", "openai/gpt-4o")

        assert isinstance(result, str)
        assert "Error" in result

    @patch('lite_client.completion')
    def test_generate_text_file_error(self, mock_completion):
        """Test handling of file not found error."""
        mock_completion.side_effect = FileNotFoundError("Image file not found")

        client = LiteClient()
        result = client.generate_text("Test", "openai/gpt-4o", image_path="/nonexistent/image.jpg")

        assert isinstance(result, dict)
        assert "error" in result

    @patch('lite_client.completion')
    def test_generate_text_unexpected_error(self, mock_completion):
        """Test handling of unexpected error."""
        mock_completion.side_effect = ValueError("Unexpected error")

        client = LiteClient()
        result = client.generate_text("Test", "openai/gpt-4o")

        assert isinstance(result, str)
        assert "Error" in result

    def test_list_models(self):
        """Test listing available models."""
        client = LiteClient()
        text_models = client.list_models("text")
        vision_models = client.list_models("vision")

        assert len(text_models) > 0
        assert len(vision_models) > 0
        assert all(isinstance(m, str) for m in text_models)
        assert all(isinstance(m, str) for m in vision_models)

    def test_get_model_by_index(self):
        """Test getting a model by index."""
        client = LiteClient()
        model = client.get_model(0, "text")

        assert model == "openai/gpt-4o"

    def test_get_model_invalid_index(self):
        """Test getting a model with invalid index."""
        client = LiteClient()
        model = client.get_model(999, "text")

        assert model is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
