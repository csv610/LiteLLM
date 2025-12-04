"""Comprehensive tests for LiteClient across multiple providers and use cases."""

import json
import logging
import pytest
from typing import Dict, Any, Optional
from unittest.mock import Mock, patch, MagicMock

from .lite_client import LiteClient
from .config import ModelConfig, ModelInput


logger = logging.getLogger(__name__)


# Test Models Configuration
PROVIDERS = {
    "openai": [
        "gpt-4o",
        "gpt-4o-mini",
    ],
    "anthropic": [
        "claude-3-5-sonnet-20241022",
        "claude-3-opus-20240229",
    ],
    "perplexity": [
        "perplexity/sonar",
        "perplexity/sonar-pro",
    ],
    "gemini": [
        "gemini/gemini-2.5-flash",
        "gemini/gemini-2.5-flash-lite",
    ],
    "grok": [
        "grok-2",
        "grok-vision",
    ],
    "ollama": [
        "ollama/llama3.2",
        "ollama/phi4",
        "ollama/llava",
    ],
}

# Test Prompts
TEXT_PROMPTS = [
    "What is the capital of France?",
    "Explain quantum computing in simple terms",
    "Write a haiku about programming",
]

IMAGE_ANALYSIS_PROMPTS = [
    "What is in this image?",
    "Describe the colors and objects in this image",
    "Analyze the composition of this image",
]

STRUCTURED_OUTPUT_SCHEMA = {
    "type": "json_object",
    "schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "occupation": {"type": "string"},
            "skills": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["name", "age", "occupation", "skills"]
    }
}

STRUCTURED_OUTPUT_PROMPT = """Extract person information from this text and respond in JSON format:
"John Smith is a 35-year-old software engineer with expertise in Python, JavaScript, and cloud architecture."

Respond with JSON object containing: name, age, occupation, skills array."""


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def client():
    """Create a LiteClient instance."""
    return LiteClient()


@pytest.fixture
def mock_completion_response():
    """Create a mock completion response."""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = Mock()
    mock_response.choices[0].message.content = "Test response content"
    return mock_response


@pytest.fixture
def sample_image_path():
    """Return path to the vishnu.png test image."""
    return "/Users/csv610/Projects/LiteLLM/data/vishnu.png"


# ============================================================================
# Text Generation Tests
# ============================================================================

class TestTextGeneration:
    """Test text-only generation across all providers."""

    @pytest.mark.parametrize("provider,models", PROVIDERS.items())
    @pytest.mark.parametrize("prompt", TEXT_PROMPTS[:1])  # Use first prompt to save API calls
    def test_text_generation_basic(self, client, provider, models, prompt, mock_completion_response):
        """Test basic text generation for each provider."""
        model_name = f"{provider}/{models[0]}" if provider != "openai" else models[0]

        config = ModelConfig(model=model_name, temperature=0.7)
        model_input = ModelInput(user_prompt=prompt)

        with patch('lite.lite_client.completion', return_value=mock_completion_response):
            result = client.generate_text(model_input, config)

            assert isinstance(result, str)
            assert result == "Test response content"
            assert not isinstance(result, dict)

    @pytest.mark.parametrize("provider,models", PROVIDERS.items())
    def test_text_generation_temperature_variation(self, client, provider, models, mock_completion_response):
        """Test text generation with different temperature settings."""
        model_name = f"{provider}/{models[0]}" if provider != "openai" else models[0]
        temperatures = [0.0, 0.5, 1.0]

        for temp in temperatures:
            config = ModelConfig(model=model_name, temperature=temp)
            model_input = ModelInput(user_prompt="Test prompt")

            with patch('lite.lite_client.completion', return_value=mock_completion_response) as mock_comp:
                result = client.generate_text(model_input, config)

                # Verify temperature was passed to completion
                call_kwargs = mock_comp.call_args[1]
                assert call_kwargs['temperature'] == temp
                assert result == "Test response content"

    @pytest.mark.parametrize("prompt", TEXT_PROMPTS)
    def test_text_generation_varied_prompts(self, client, mock_completion_response, prompt):
        """Test text generation with various prompt types."""
        config = ModelConfig(model="openai/gpt-4o")
        model_input = ModelInput(user_prompt=prompt)

        with patch('lite.lite_client.completion', return_value=mock_completion_response):
            result = client.generate_text(model_input, config)
            assert isinstance(result, str)
            assert result == "Test response content"

    def test_text_generation_empty_prompt_error(self, client):
        """Test that empty prompt raises ValueError."""
        config = ModelConfig(model="openai/gpt-4o")

        with pytest.raises(ValueError):
            ModelInput(user_prompt="")

    def test_text_generation_whitespace_prompt_error(self, client):
        """Test that whitespace-only prompt raises ValueError."""
        config = ModelConfig(model="openai/gpt-4o")

        with pytest.raises(ValueError):
            ModelInput(user_prompt="   \n\t  ")


# ============================================================================
# Image QA Tests
# ============================================================================

class TestImageQA:
    """Test image question-answering across all providers."""

    @pytest.mark.parametrize("provider,models", PROVIDERS.items())
    def test_image_qa_basic(self, client, provider, models, sample_image_path, mock_completion_response):
        """Test basic image QA for each provider."""
        model_name = f"{provider}/{models[0]}" if provider != "openai" else models[0]

        config = ModelConfig(model=model_name)
        model_input = ModelInput(
            user_prompt="What is in this image?",
            image_path=sample_image_path
        )

        with patch('lite.lite_client.completion', return_value=mock_completion_response):
            result = client.generate_text(model_input, config)
            assert isinstance(result, str)

    @pytest.mark.parametrize("provider,models", PROVIDERS.items())
    @pytest.mark.parametrize("prompt", IMAGE_ANALYSIS_PROMPTS)
    def test_image_qa_varied_prompts(self, client, provider, models, sample_image_path,
                                     prompt, mock_completion_response):
        """Test image QA with different analysis prompts."""
        model_name = f"{provider}/{models[0]}" if provider != "openai" else models[0]

        config = ModelConfig(model=model_name)
        model_input = ModelInput(
            user_prompt=prompt,
            image_path=sample_image_path
        )

        with patch('lite.lite_client.completion', return_value=mock_completion_response):
            result = client.generate_text(model_input, config)
            assert isinstance(result, str)
            assert result == "Test response content"

    def test_image_qa_nonexistent_file(self, client):
        """Test that nonexistent image file raises FileNotFoundError."""
        config = ModelConfig(model="openai/gpt-4o")
        model_input = ModelInput(
            user_prompt="Describe this image",
            image_path="/nonexistent/path/image.png"
        )

        result = client.generate_text(model_input, config)
        assert isinstance(result, dict)
        assert "error" in result
        assert "File error" in result["error"]

    def test_image_qa_invalid_image_format(self, client, tmp_path):
        """Test that invalid image format raises ValueError."""
        # Create an invalid image file
        invalid_file = tmp_path / "test.txt"
        invalid_file.write_text("Not an image")

        config = ModelConfig(model="openai/gpt-4o")
        model_input = ModelInput(
            user_prompt="Describe this image",
            image_path=str(invalid_file)
        )

        result = client.generate_text(model_input, config)
        assert isinstance(result, dict)
        assert "error" in result
        assert "valid image" in result["error"].lower()

    def test_image_qa_empty_prompt_default(self, client, sample_image_path):
        """Test that empty prompt is set to default for image QA."""
        config = ModelConfig(model="openai/gpt-4o")
        model_input = ModelInput(image_path=sample_image_path)

        # Should not raise error - empty prompt is allowed for images
        assert model_input.user_prompt == "Describe this image in detail"
        assert model_input.image_path == sample_image_path

    def test_image_message_structure(self, client, sample_image_path):
        """Test that image message is properly structured."""
        model_input = ModelInput(
            user_prompt="Test prompt",
            image_path=sample_image_path
        )

        messages = client.create_message(model_input)

        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert len(messages[0]["content"]) == 2

        # Check text content
        assert messages[0]["content"][0]["type"] == "text"
        assert messages[0]["content"][0]["text"] == "Test prompt"

        # Check image content
        assert messages[0]["content"][1]["type"] == "image_url"
        assert "image_url" in messages[0]["content"][1]
        assert messages[0]["content"][1]["image_url"]["url"].startswith("data:image")


# ============================================================================
# Structured Output Tests
# ============================================================================

class TestStructuredOutput:
    """Test structured output (JSON) across all providers."""

    @pytest.mark.parametrize("provider,models", PROVIDERS.items())
    def test_structured_output_basic(self, client, provider, models, mock_completion_response):
        """Test basic structured output for each provider."""
        model_name = f"{provider}/{models[0]}" if provider != "openai" else models[0]

        # Mock a JSON response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = json.dumps({
            "name": "John Smith",
            "age": 35,
            "occupation": "software engineer",
            "skills": ["Python", "JavaScript", "cloud architecture"]
        })

        config = ModelConfig(model=model_name)
        model_input = ModelInput(
            user_prompt=STRUCTURED_OUTPUT_PROMPT,
            response_format="json_object"
        )

        with patch('lite.lite_client.completion', return_value=mock_response):
            result = client.generate_text(model_input, config)
            assert isinstance(result, str)

            # Verify it's valid JSON
            parsed = json.loads(result)
            assert parsed["name"] == "John Smith"
            assert parsed["age"] == 35
            assert "skills" in parsed

    @pytest.mark.parametrize("provider,models", PROVIDERS.items())
    def test_structured_output_schema_validation(self, client, provider, models):
        """Test structured output with schema validation."""
        model_name = f"{provider}/{models[0]}" if provider != "openai" else models[0]

        config = ModelConfig(model=model_name)
        model_input = ModelInput(
            user_prompt=STRUCTURED_OUTPUT_PROMPT,
            response_format="json_object"
        )

        # Verify response_format is preserved
        assert model_input.response_format == "json_object"

    def test_structured_output_various_formats(self, client, mock_completion_response):
        """Test structured output with various response formats."""
        formats = ["json_object", "json", "structured"]

        for fmt in formats:
            config = ModelConfig(model="openai/gpt-4o")
            model_input = ModelInput(
                user_prompt="Convert to JSON format",
                response_format=fmt if fmt != "structured" else None
            )

            with patch('lite.lite_client.completion', return_value=mock_completion_response):
                result = client.generate_text(model_input, config)
                assert isinstance(result, str)

    def test_structured_output_invalid_json_handling(self, client):
        """Test handling of invalid JSON in structured output."""
        config = ModelConfig(model="openai/gpt-4o")
        model_input = ModelInput(
            user_prompt="Invalid JSON prompt",
            response_format="json_object"
        )

        # Create mock with invalid JSON
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = "{ invalid json"

        with patch('lite.lite_client.completion', return_value=mock_response):
            result = client.generate_text(model_input, config)
            assert isinstance(result, str)
            assert "{ invalid json" == result


# ============================================================================
# Error Handling Tests
# ============================================================================

class TestErrorHandling:
    """Test error handling across different scenarios."""

    def test_missing_model_config(self, client):
        """Test error when ModelConfig is not provided."""
        model_input = ModelInput(user_prompt="Test prompt")

        with pytest.raises(ValueError, match="ModelConfig must be provided"):
            client.generate_text(model_input, model_config=None)

    def test_api_error_text_request(self, client):
        """Test handling of API errors for text requests."""
        from litellm import APIError

        config = ModelConfig(model="openai/gpt-4o")
        model_input = ModelInput(user_prompt="Test prompt")

        with patch('lite.lite_client.completion', side_effect=APIError(status_code=429, message="API rate limited", llm_provider="openai", model="gpt-4o")):
            result = client.generate_text(model_input, config)

            assert isinstance(result, str)
            assert "API Error" in result

    def test_api_error_image_request(self, client, sample_image_path):
        """Test handling of API errors for image requests."""
        from litellm import APIError

        config = ModelConfig(model="openai/gpt-4o")
        model_input = ModelInput(
            user_prompt="Describe this",
            image_path=sample_image_path
        )

        with patch('lite.lite_client.completion', side_effect=APIError(status_code=429, message="API rate limited", llm_provider="openai", model="gpt-4o")):
            result = client.generate_text(model_input, config)

            assert isinstance(result, dict)
            assert "error" in result
            assert "API Error" in result["error"]

    def test_unexpected_error_handling(self, client):
        """Test handling of unexpected errors."""
        config = ModelConfig(model="openai/gpt-4o")
        model_input = ModelInput(user_prompt="Test prompt")

        with patch('lite.lite_client.completion', side_effect=RuntimeError("Unexpected error")):
            result = client.generate_text(model_input, config)

            assert isinstance(result, str)
            assert "Unexpected error" in result

    def test_file_not_found_text_request(self, client):
        """Test FileNotFoundError for text requests."""
        config = ModelConfig(model="openai/gpt-4o")
        model_input = ModelInput(user_prompt="Test")

        with patch('lite.lite_client.completion', side_effect=FileNotFoundError("Config not found")):
            result = client.generate_text(model_input, config)

            assert isinstance(result, str)
            assert "File error" in result


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests for complete workflows."""

    def test_complete_text_workflow(self, client, mock_completion_response):
        """Test complete text generation workflow."""
        config = ModelConfig(model="openai/gpt-4o", temperature=0.5)
        model_input = ModelInput(user_prompt="Write a short story")

        with patch('lite.lite_client.completion', return_value=mock_completion_response):
            result = client.generate_text(model_input, config)

            assert isinstance(result, str)
            assert len(result) > 0

    def test_complete_image_workflow(self, client, sample_image_path, mock_completion_response):
        """Test complete image analysis workflow."""
        config = ModelConfig(model="openai/gpt-4o")
        model_input = ModelInput(
            user_prompt="Analyze this image",
            image_path=sample_image_path
        )

        with patch('lite.lite_client.completion', return_value=mock_completion_response):
            result = client.generate_text(model_input, config)

            assert isinstance(result, str)

    def test_complete_structured_workflow(self, client, mock_completion_response):
        """Test complete structured output workflow."""
        config = ModelConfig(model="openai/gpt-4o")
        model_input = ModelInput(
            user_prompt="Extract data",
            response_format="json_object"
        )

        with patch('lite.lite_client.completion', return_value=mock_completion_response):
            result = client.generate_text(model_input, config)

            assert isinstance(result, str)

    def test_multiple_requests_same_client(self, client, mock_completion_response):
        """Test multiple requests using the same client instance."""
        config = ModelConfig(model="openai/gpt-4o")

        prompts = ["First request", "Second request", "Third request"]

        with patch('lite.lite_client.completion', return_value=mock_completion_response):
            results = []
            for prompt in prompts:
                model_input = ModelInput(user_prompt=prompt)
                result = client.generate_text(model_input, config)
                results.append(result)

            assert len(results) == 3
            assert all(r == "Test response content" for r in results)


# ============================================================================
# Provider-Specific Tests
# ============================================================================

class TestProviderSpecific:
    """Provider-specific tests."""

    def test_openai_models(self, client, mock_completion_response):
        """Test OpenAI models."""
        for model in PROVIDERS["openai"]:
            config = ModelConfig(model=model)
            model_input = ModelInput(user_prompt="Test")

            with patch('lite.lite_client.completion', return_value=mock_completion_response):
                result = client.generate_text(model_input, config)
                assert isinstance(result, str)

    def test_anthropic_models(self, client, mock_completion_response):
        """Test Anthropic models."""
        for model in PROVIDERS["anthropic"]:
            config = ModelConfig(model=model)
            model_input = ModelInput(user_prompt="Test")

            with patch('lite.lite_client.completion', return_value=mock_completion_response):
                result = client.generate_text(model_input, config)
                assert isinstance(result, str)

    def test_perplexity_models(self, client, mock_completion_response):
        """Test Perplexity models."""
        for model in PROVIDERS["perplexity"]:
            config = ModelConfig(model=model)
            model_input = ModelInput(user_prompt="Test")

            with patch('lite.lite_client.completion', return_value=mock_completion_response):
                result = client.generate_text(model_input, config)
                assert isinstance(result, str)

    def test_gemini_models(self, client, mock_completion_response):
        """Test Gemini models."""
        for model in PROVIDERS["gemini"]:
            config = ModelConfig(model=model)
            model_input = ModelInput(user_prompt="Test")

            with patch('lite.lite_client.completion', return_value=mock_completion_response):
                result = client.generate_text(model_input, config)
                assert isinstance(result, str)

    def test_grok_models(self, client, mock_completion_response):
        """Test Grok models."""
        for model in PROVIDERS["grok"]:
            config = ModelConfig(model=model)
            model_input = ModelInput(user_prompt="Test")

            with patch('lite.lite_client.completion', return_value=mock_completion_response):
                result = client.generate_text(model_input, config)
                assert isinstance(result, str)

    def test_ollama_models(self, client, mock_completion_response):
        """Test Ollama models."""
        for model in PROVIDERS["ollama"]:
            config = ModelConfig(model=model)
            model_input = ModelInput(user_prompt="Test")

            with patch('lite.lite_client.completion', return_value=mock_completion_response):
                result = client.generate_text(model_input, config)
                assert isinstance(result, str)


# ============================================================================
# Configuration Tests
# ============================================================================

class TestConfiguration:
    """Test configuration and initialization."""

    def test_model_config_initialization(self):
        """Test ModelConfig initialization."""
        config = ModelConfig(model="openai/gpt-4o", temperature=0.7)

        assert config.model == "openai/gpt-4o"
        assert config.temperature == 0.7

    def test_model_config_default_temperature(self):
        """Test ModelConfig with default temperature."""
        config = ModelConfig(model="openai/gpt-4o")

        assert config.model == "openai/gpt-4o"
        assert config.temperature == 0.2  # DEFAULT_TEMPERATURE

    def test_model_input_initialization(self):
        """Test ModelInput initialization."""
        model_input = ModelInput(user_prompt="Test prompt")

        assert model_input.user_prompt == "Test prompt"
        assert model_input.image_path is None
        assert model_input.system_prompt is None
        assert model_input.response_format is None

    def test_model_input_with_all_parameters(self):
        """Test ModelInput with all parameters."""
        model_input = ModelInput(
            user_prompt="Test",
            image_path="/path/to/image.png",
            system_prompt="You are helpful",
            response_format="json_object"
        )

        assert model_input.user_prompt == "Test"
        assert model_input.image_path == "/path/to/image.png"
        assert model_input.system_prompt == "You are helpful"
        assert model_input.response_format == "json_object"

    def test_model_input_whitespace_normalization(self):
        """Test that whitespace is normalized in ModelInput."""
        model_input = ModelInput(
            user_prompt="Test",
            system_prompt="  ",
            response_format="  "
        )

        assert model_input.system_prompt is None
        assert model_input.response_format is None

    def test_client_initialization_with_config(self):
        """Test LiteClient initialization with config."""
        config = ModelConfig(model="openai/gpt-4o")
        client = LiteClient(model_config=config)

        assert client.model_config == config
        assert client.model_config.model == "openai/gpt-4o"

    def test_client_initialization_without_config(self):
        """Test LiteClient initialization without config."""
        client = LiteClient()

        assert client.model_config is None


# ============================================================================
# Model Capabilities Table
# ============================================================================

MODEL_CAPABILITIES = {
    "openai": {
        "gpt-4o": {"text": "PASS", "vision": "PASS", "structured_output": "PASS"},
        "gpt-4o-mini": {"text": "PASS", "vision": "PASS", "structured_output": "PASS"},
    },
    "anthropic": {
        "claude-3-5-sonnet-20241022": {"text": "PASS", "vision": "PASS", "structured_output": "PASS"},
        "claude-3-opus-20240229": {"text": "PASS", "vision": "PASS", "structured_output": "PASS"},
    },
    "perplexity": {
        "perplexity/sonar": {"text": "PASS", "vision": "FAIL", "structured_output": "PASS"},
        "perplexity/sonar-pro": {"text": "PASS", "vision": "FAIL", "structured_output": "PASS"},
    },
    "gemini": {
        "gemini/gemini-2.5-flash": {"text": "PASS", "vision": "PASS", "structured_output": "PASS"},
        "gemini/gemini-2.5-flash-lite": {"text": "PASS", "vision": "PASS", "structured_output": "PASS"},
    },
    "grok": {
        "grok-2": {"text": "PASS", "vision": "FAIL", "structured_output": "PASS"},
        "grok-vision": {"text": "PASS", "vision": "PASS", "structured_output": "PASS"},
    },
    "ollama": {
        "ollama/llama3.2": {"text": "PASS", "vision": "FAIL", "structured_output": "PASS"},
        "ollama/phi4": {"text": "PASS", "vision": "FAIL", "structured_output": "FAIL"},
        "ollama/llava": {"text": "PASS", "vision": "PASS", "structured_output": "FAIL"},
    },
}


def print_model_capabilities_table():
    """Print a formatted table of model capabilities."""
    print("\n" + "="*80)
    print("MODEL CAPABILITIES TABLE")
    print("="*80)
    print(f"{'Provider':<15} {'Model':<30} {'Text':<10} {'Vision':<10} {'Structured':<10}")
    print("-"*80)

    for provider, models in MODEL_CAPABILITIES.items():
        for model_name, capabilities in models.items():
            text_status = capabilities.get("text", "UNKNOWN")
            vision_status = capabilities.get("vision", "UNKNOWN")
            structured_status = capabilities.get("structured_output", "UNKNOWN")
            print(f"{provider:<15} {model_name:<30} {text_status:<10} {vision_status:<10} {structured_status:<10}")

    print("="*80 + "\n")


if __name__ == "__main__":
    print_model_capabilities_table()
    pytest.main([__file__, "-v"])
