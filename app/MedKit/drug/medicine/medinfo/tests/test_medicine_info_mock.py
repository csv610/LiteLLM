from pathlib import Path
from unittest.mock import patch

import pytest
from lite.config import ModelConfig
from medicine_info import MedicineInfoGenerator


@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@patch("medicine_info.LiteClient")
def test_medicine_info_mock(mock_client_class, mock_model_config):
    mock_client_instance = mock_client_class.return_value
    raw_markdown = "# Medicine Info for Aspirin"
    mock_client_instance.generate_text.return_value = raw_markdown
    
    generator = MedicineInfoGenerator(mock_model_config)
    result = generator.generate_text("Aspirin")
    
    assert result == raw_markdown
    mock_client_instance.generate_text.assert_called_once()
    
    # Verify ModelInput
    args, kwargs = mock_client_instance.generate_text.call_args
    model_input = kwargs.get("model_input") or args[0]
    assert "Aspirin" in model_input.user_prompt

def test_medicine_info_validation(mock_model_config):
    generator = MedicineInfoGenerator(mock_model_config)
    with pytest.raises(ValueError, match="Medicine name cannot be empty"):
        generator.generate_text("")
    with pytest.raises(ValueError, match="Medicine name cannot be empty"):
        generator.generate_text("   ")

@patch("medicine_info.save_model_response")
def test_save_mock(mock_save_response, mock_model_config):
    generator = MedicineInfoGenerator(mock_model_config)
    result = "# Info"
    output_path = Path("outputs/aspirin.md")
    
    generator.save(result, output_path)
    
    mock_save_response.assert_called_once_with(result, output_path)
