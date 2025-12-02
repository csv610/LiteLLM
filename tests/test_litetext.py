"""Tests for LiteClient and ModelConfig modules."""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add root directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput


class TestModelConfig:
    """Test ModelConfig class."""

    def test_create_model_config(self):
        """Test creating a ModelConfig instance."""
        config = ModelConfig(model="openai/gpt-4o", temperature=0.5)
        assert config.model == "openai/gpt-4o"
        assert config.temperature == 0.5

    def test_create_model_input_with_prompt(self):
        """Test creating a ModelInput with a prompt."""
        input_obj = ModelInput(user_prompt="Hello")
        assert input_obj.user_prompt == "Hello"
        assert input_obj.image_path is None

    def test_create_model_input_with_image(self):
        """Test creating a ModelInput with image path."""
        input_obj = ModelInput(user_prompt="Describe", image_path="/path/to/image.jpg")
        assert input_obj.user_prompt == "Describe"
        assert input_obj.image_path == "/path/to/image.jpg"

    def test_model_input_empty_prompt_no_image_raises_error(self):
        """Test that empty prompt without image raises error."""
        with pytest.raises(ValueError):
            ModelInput(user_prompt="")

    def test_model_input_empty_prompt_with_image_uses_default(self):
        """Test that empty prompt with image uses default."""
        input_obj = ModelInput(user_prompt="", image_path="/path/to/image.jpg")
        assert input_obj.user_prompt == "Describe this image in detail"

    def test_model_input_whitespace_prompt_no_image_raises_error(self):
        """Test that whitespace-only prompt without image raises error."""
        with pytest.raises(ValueError):
            ModelInput(user_prompt="   ")

    def test_model_input_system_prompt_normalization(self):
        """Test that empty system_prompt is normalized to None."""
        input_obj = ModelInput(user_prompt="Test", system_prompt="")
        assert input_obj.system_prompt is None

    def test_model_input_response_format_normalization(self):
        """Test that empty response_format is normalized to None."""
        input_obj = ModelInput(user_prompt="Test", response_format="")
        assert input_obj.response_format is None

    def test_model_input_with_response_format(self):
        """Test creating a ModelInput with response_format."""
        input_obj = ModelInput(user_prompt="Test", response_format="json")
        assert input_obj.user_prompt == "Test"
        assert input_obj.response_format == "json"


class TestLiteClient:
    """Test LiteClient class."""

    def test_create_message_text_only(self):
        """Test creating a message with text only."""
        prompt = "What is AI?"
        model_input = ModelInput(user_prompt=prompt)
        message = LiteClient.create_message(model_input)

        assert isinstance(message, list)
        assert len(message) == 1
        assert message[0]["role"] == "user"
        assert len(message[0]["content"]) == 1
        assert message[0]["content"][0]["type"] == "text"
        assert message[0]["content"][0]["text"] == prompt

    @patch('lite.image_utils.ImageUtils.encode_to_base64')
    def test_create_message_with_image(self, mock_encode):
        """Test creating a message with text and image."""
        mock_encode.return_value = "data:image/jpeg;base64,fake_base64_data"

        prompt = "Describe this image"
        image_path = "/path/to/image.jpg"
        model_input = ModelInput(user_prompt=prompt, image_path=image_path)
        message = LiteClient.create_message(model_input)

        assert isinstance(message, list)
        assert len(message) == 1
        assert message[0]["role"] == "user"
        assert len(message[0]["content"]) == 2
        assert message[0]["content"][0]["type"] == "text"
        assert message[0]["content"][1]["type"] == "image_url"

    def test_generate_text_empty_prompt_no_image(self):
        """Test that empty prompt without image returns error."""
        client = LiteClient()
        model_config = ModelConfig(model="openai/gpt-4o")

        with pytest.raises(ValueError):
            model_input = ModelInput(user_prompt="")
            client.generate_text(model_input, model_config)

    def test_generate_text_whitespace_only_prompt_no_image(self):
        """Test that whitespace-only prompt without image returns error."""
        client = LiteClient()
        model_config = ModelConfig(model="openai/gpt-4o")

        with pytest.raises(ValueError):
            model_input = ModelInput(user_prompt="   ")
            client.generate_text(model_input, model_config)

    def test_generate_text_empty_prompt_with_image(self):
        """Test that empty prompt with image uses default prompt."""
        client = LiteClient()
        model_config = ModelConfig(model="openai/gpt-4o")

        with patch('lite.lite_client.completion') as mock_completion:
            with patch('lite.image_utils.ImageUtils.encode_to_base64'):
                mock_response = MagicMock()
                mock_response.choices[0].message.content = "Image description"
                mock_completion.return_value = mock_response

                model_input = ModelInput(user_prompt="", image_path="/path/to/image.jpg")
                result = client.generate_text(model_input, model_config)

                assert result == "Image description"
                # Verify that completion was called with default prompt
                mock_completion.assert_called_once()

    @patch('lite.lite_client.completion')
    def test_generate_text_success(self, mock_completion):
        """Test successful text generation."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "This is a test response"
        mock_completion.return_value = mock_response

        client = LiteClient()
        model_config = ModelConfig(model="openai/gpt-4o")
        model_input = ModelInput(user_prompt="Test prompt")
        result = client.generate_text(model_input, model_config)

        assert result == "This is a test response"
        mock_completion.assert_called_once()

    @patch('lite.lite_client.completion')
    def test_generate_text_with_custom_temperature(self, mock_completion):
        """Test text generation with custom temperature."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Response"
        mock_completion.return_value = mock_response

        client = LiteClient()
        model_config = ModelConfig(model="openai/gpt-4o", temperature=0.8)
        model_input = ModelInput(user_prompt="Test")
        client.generate_text(model_input, model_config)

        mock_completion.assert_called_once()
        call_kwargs = mock_completion.call_args[1]
        assert call_kwargs["temperature"] == 0.8

    @patch('lite.lite_client.completion')
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
        model_config = ModelConfig(model="openai/gpt-4o")
        model_input = ModelInput(user_prompt="Test")
        result = client.generate_text(model_input, model_config)

        assert isinstance(result, str)
        assert "Error" in result

    @patch('lite.lite_client.completion')
    def test_generate_text_file_error(self, mock_completion):
        """Test handling of file not found error."""
        mock_completion.side_effect = FileNotFoundError("Image file not found")

        client = LiteClient()
        model_config = ModelConfig(model="openai/gpt-4o")
        model_input = ModelInput(user_prompt="Test", image_path="/nonexistent/image.jpg")
        result = client.generate_text(model_input, model_config)

        assert isinstance(result, dict)
        assert "error" in result

    @patch('lite.lite_client.completion')
    def test_generate_text_unexpected_error(self, mock_completion):
        """Test handling of unexpected error."""
        mock_completion.side_effect = RuntimeError("Unexpected error")

        client = LiteClient()
        model_config = ModelConfig(model="openai/gpt-4o")
        model_input = ModelInput(user_prompt="Test")
        result = client.generate_text(model_input, model_config)

        assert isinstance(result, str)
        assert "error" in result.lower()

    @patch('lite.lite_client.completion')
    def test_generate_text_with_response_format(self, mock_completion):
        """Test text generation with response_format."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '{"result": "JSON response"}'
        mock_completion.return_value = mock_response

        client = LiteClient()
        model_config = ModelConfig(model="openai/gpt-4o")
        model_input = ModelInput(user_prompt="Generate JSON", response_format="json")
        result = client.generate_text(model_input, model_config)

        assert result == '{"result": "JSON response"}'
        mock_completion.assert_called_once()
        call_kwargs = mock_completion.call_args[1]
        assert call_kwargs["response_format"] == "json"

    @patch('lite.lite_client.completion')
    def test_generate_text_with_response_format_none(self, mock_completion):
        """Test that None response_format is passed correctly."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Regular response"
        mock_completion.return_value = mock_response

        client = LiteClient()
        model_config = ModelConfig(model="openai/gpt-4o")
        model_input = ModelInput(user_prompt="Test", response_format=None)
        result = client.generate_text(model_input, model_config)

        assert result == "Regular response"
        mock_completion.assert_called_once()
        call_kwargs = mock_completion.call_args[1]
        assert call_kwargs["response_format"] is None



if __name__ == "__main__":
    pytest.main([__file__, "-v"])
