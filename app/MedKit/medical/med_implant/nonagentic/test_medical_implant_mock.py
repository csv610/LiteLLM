import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.med_implant.agentic.medical_implant import MedicalImplantGenerator
from medical.med_implant.agentic.medical_implant_models import ModelOutput


@pytest.fixture
def model_config():
    return ModelConfig(model="test-model")


@pytest.fixture
def generator(model_config):
    with patch("medical.med_implant.agentic.medical_implant.LiteClient"):
        gen = MedicalImplantGenerator(model_config)
        return gen


def test_generate_text_invalid_input(generator):
    with pytest.raises(ValueError, match="Implant name cannot be empty"):
        generator.generate_text("")

    with pytest.raises(ValueError, match="Implant name cannot be empty"):
        generator.generate_text("  ")


@patch("medical.med_implant.agentic.medical_implant.PromptBuilder")
def test_generate_text_success(mock_prompt_builder, generator):
    # Setup mocks
    mock_prompt_builder.create_system_prompt.return_value = "system prompt"
    mock_prompt_builder.create_user_prompt.return_value = "user prompt"

    mock_output = ModelOutput(markdown="Some content")
    generator.client.generate_text.return_value = mock_output

    # Execute
    result = generator.generate_text("Pacemaker")

    # Assert
    assert result == mock_output
    assert generator.implant == "Pacemaker"
    generator.client.generate_text.assert_called_once()


def test_save(generator, tmp_path):
    # Setup
    generator.implant = "Pacemaker"
    mock_result = ModelOutput(markdown="content")

    with patch("medical.med_implant.agentic.medical_implant.save_model_response") as mock_save:
        mock_save.return_value = tmp_path / "pacemaker.md"

        # Execute
        path = generator.save(mock_result, tmp_path)

        # Assert
        assert path == tmp_path / "pacemaker.md"
        mock_save.assert_called_once_with(mock_result, tmp_path / "pacemaker")


def test_save_no_implant(generator, tmp_path):
    mock_result = ModelOutput(markdown="content")
    with pytest.raises(ValueError, match="No implant information available"):
        generator.save(mock_result, tmp_path)
