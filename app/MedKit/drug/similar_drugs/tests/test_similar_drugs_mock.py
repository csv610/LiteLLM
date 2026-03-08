import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

from similar_drugs import SimilarDrugs
from similar_drugs_models import SimilarDrugsConfig, SimilarMedicinesResult
from lite.config import ModelConfig, ModelInput

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def mock_similar_drugs_config():
    return SimilarDrugsConfig(verbosity=0)

@patch("similar_drugs.LiteClient")
def test_similar_drugs_mock(mock_client_class, mock_model_config, mock_similar_drugs_config):
    mock_client_instance = mock_client_class.return_value
    raw_markdown = "# Similar Medicines for Aspirin"
    mock_client_instance.generate_text.return_value = raw_markdown
    
    finder = SimilarDrugs(mock_similar_drugs_config, mock_model_config)
    result = finder.find("Aspirin")
    
    assert result == raw_markdown
    mock_client_instance.generate_text.assert_called_once()
    
    # Verify ModelInput
    args, kwargs = mock_client_instance.generate_text.call_args
    model_input = kwargs.get("model_input") or args[0]
    assert "Aspirin" in model_input.user_prompt

def test_similar_drugs_validation(mock_model_config, mock_similar_drugs_config):
    finder = SimilarDrugs(mock_similar_drugs_config, mock_model_config)
    with pytest.raises(ValueError, match="Medicine name cannot be empty"):
        finder.find("")
    with pytest.raises(ValueError, match="Age must be between 0 and 150 years"):
        finder.find("Aspirin", patient_age=200)
