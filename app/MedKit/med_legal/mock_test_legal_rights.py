from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from lite.config import ModelConfig

try:
    from med_legal.legal_rights import LegalRightsGenerator
    from med_legal.legal_rights_models import LegalRightsModel, ModelOutput
    from med_legal.legal_rights_prompts import PromptBuilder
except ImportError:
    from legal_rights import LegalRightsGenerator
    from legal_rights_models import LegalRightsModel, ModelOutput
    from legal_rights_prompts import PromptBuilder


def test_prompt_builder():
    sys_prompt = PromptBuilder.create_system_prompt()
    assert "You are a legal expert specializing in patient rights" in sys_prompt
    assert "Legal Overview and Basis" in sys_prompt

    user_prompt = PromptBuilder.create_user_prompt("Informed Consent", "USA")
    assert "Informed Consent" in user_prompt
    assert "USA" in user_prompt


def test_generator_init():
    with patch("legal_rights.LiteClient") as mock_client:
        config = ModelConfig(model="test-model")
        gen = LegalRightsGenerator(config)
        assert gen.model_config == config
        mock_client.assert_called_once_with(config)
        assert gen.topic is None


def test_generate_text_success():
    with patch("legal_rights.LiteClient"):
        config = ModelConfig(model="test-model")
        gen = LegalRightsGenerator(config)

        # Setup mock
        mock_output = ModelOutput(markdown="Test Markdown")
        gen.client = MagicMock()
        gen.client.generate_text.return_value = mock_output

        result = gen.generate_text(topic="Privacy", country="Canada", structured=False)

        assert result == mock_output
        assert gen.topic == "Privacy"

        # Check what was passed to generate_text
        call_args = gen.client.generate_text.call_args[1]
        model_input = call_args["model_input"]
        assert "Privacy" in model_input.user_prompt
        assert "Canada" in model_input.user_prompt
        assert model_input.response_format is None


def test_generate_text_structured():
    with patch("legal_rights.LiteClient"):
        config = ModelConfig(model="test-model")
        gen = LegalRightsGenerator(config)

        # Setup mock
        mock_output = ModelOutput(markdown="Test Markdown")
        gen.client = MagicMock()
        gen.client.generate_text.return_value = mock_output

        gen.generate_text(topic="Privacy", country="Canada", structured=True)

        call_args = gen.client.generate_text.call_args[1]
        model_input = call_args["model_input"]
        assert model_input.response_format == LegalRightsModel


def test_generate_text_empty_topic():
    with patch("legal_rights.LiteClient"):
        config = ModelConfig(model="test-model")
        gen = LegalRightsGenerator(config)

        with pytest.raises(ValueError, match="Topic name cannot be empty"):
            gen.generate_text(topic="", country="USA")


def test_generate_text_empty_country():
    with patch("legal_rights.LiteClient"):
        config = ModelConfig(model="test-model")
        gen = LegalRightsGenerator(config)

        with pytest.raises(ValueError, match="Country cannot be empty"):
            gen.generate_text(topic="Topic", country="")


@patch("legal_rights.save_model_response")
def test_save(mock_save_response, tmp_path):
    with patch("legal_rights.LiteClient"):
        config = ModelConfig(model="test-model")
        gen = LegalRightsGenerator(config)

        # Need to generate text first to set the topic
        mock_output = ModelOutput(markdown="Test Markdown")
        gen.client = MagicMock()
        gen.client.generate_text.return_value = mock_output
        gen.generate_text(topic="Privacy", country="UK")

        gen.save(mock_output, tmp_path, user_name="TestUser")

        mock_save_response.assert_called_once()

        # Assert filename starts with safe username and ends with something like complain_...
        call_args = mock_save_response.call_args[0]
        path_arg = call_args[1]
        assert path_arg.parent == tmp_path
        assert "testuser_complain_" in path_arg.name


def test_save_without_topic():
    with patch("legal_rights.LiteClient"):
        config = ModelConfig(model="test-model")
        gen = LegalRightsGenerator(config)

        mock_output = ModelOutput(markdown="Test Markdown")
        with pytest.raises(ValueError, match="No topic information available"):
            gen.save(mock_output, Path("."), "TestUser")
