import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

from symptom_drugs import SymptomDrugs
from symptom_drugs_prompts import SymptomInput
from symptom_drugs_models import SymptomDrugAnalysisModel
from lite.config import ModelConfig, ModelInput

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@patch("symptom_drugs.LiteClient")
def test_symptoms_drugs_mock(mock_client_class, mock_model_config):
    mock_client_instance = mock_client_class.return_value
    raw_markdown = "# Medications for Headache"
    mock_client_instance.generate_text.return_value = raw_markdown
    
    analyzer = SymptomDrugs(mock_model_config)
    config = SymptomInput(symptom_name="Headache")
    result = analyzer.generate_text(config)
    
    assert result == raw_markdown
    mock_client_instance.generate_text.assert_called_once()
    
    # Verify ModelInput
    args, kwargs = mock_client_instance.generate_text.call_args
    model_input = kwargs.get("model_input") or args[0]
    assert "Headache" in model_input.user_prompt

@patch("symptom_drugs.save_model_response")
def test_save_mock(mock_save_response, mock_model_config):
    analyzer = SymptomDrugs(mock_model_config)
    config = SymptomInput(symptom_name="Headache")
    analyzer.config = config
    result = "# Info"
    output_dir = Path("test_outputs")
    
    analyzer.save(result, output_dir)
    
    mock_save_response.assert_called_once()
    args, _ = mock_save_response.call_args
    assert args[0] == result
    assert "headache_drug_recommendations" in str(args[1])
