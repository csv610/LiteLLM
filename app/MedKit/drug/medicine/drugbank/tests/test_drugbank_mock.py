import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

from drugbank_medicine import DrugBankMedicine
from drugbank_medicine_models import MedicineInfo
from lite.config import ModelConfig, ModelInput

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@patch("drugbank_medicine.LiteClient")
def test_drugbank_medicine_mock(mock_client_class, mock_model_config):
    mock_client_instance = mock_client_class.return_value
    raw_markdown = "# Medicine Info for Aspirin"
    mock_client_instance.generate_text.return_value = raw_markdown
    
    fetcher = DrugBankMedicine(mock_model_config)
    result = fetcher.generate_text("Aspirin")
    
    assert result == raw_markdown
    mock_client_instance.generate_text.assert_called_once()
    
    # Verify ModelInput
    args, kwargs = mock_client_instance.generate_text.call_args
    model_input = kwargs.get("model_input") or args[0]
    assert "Aspirin" in model_input.user_prompt

def test_drugbank_medicine_validation(mock_model_config):
    fetcher = DrugBankMedicine(mock_model_config)
    with pytest.raises(ValueError, match="Medicine name cannot be empty"):
        fetcher.generate_text("")
    with pytest.raises(ValueError, match="Medicine name cannot be empty"):
        fetcher.generate_text("   ")

@patch("drugbank_medicine.save_model_response")
def test_save_mock(mock_save_response, mock_model_config):
    fetcher = DrugBankMedicine(mock_model_config)
    fetcher.medicine_name = "Aspirin"
    result = "# Info"
    output_dir = Path("test_outputs")
    
    fetcher.save(result, output_dir)
    
    mock_save_response.assert_called_once()
    args, _ = mock_save_response.call_args
    assert args[0] == result
    assert "Aspirin_medicine_info" in str(args[1])
