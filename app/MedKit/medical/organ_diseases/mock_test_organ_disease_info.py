import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pytest
from unittest.mock import patch, MagicMock
from medical.organ_diseases.organ_disease_info import DiseaseInfoGenerator
from lite.config import ModelConfig
from medical.organ_diseases.organ_disease_info_models import (
    OrganDiseasesModel, ModelOutput
)

@pytest.fixture
def mock_lite_client():
    with patch('medical.organ_diseases.organ_disease_info.LiteClient') as mock:
        yield mock

def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = DiseaseInfoGenerator(config)
    assert generator.model_config == config

def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = DiseaseInfoGenerator(config)
    mock_output = ModelOutput(markdown="Heart diseases", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    result = generator.generate_text("Heart")
    assert result.markdown == "Heart diseases"
    assert generator.organ == "Heart"

def test_generate_text_empty():
    config = ModelConfig(model="test-model")
    generator = DiseaseInfoGenerator(config)
    with pytest.raises(ValueError, match="Organ name cannot be empty"):
        generator.generate_text("")

def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = DiseaseInfoGenerator(config)
    
    mock_data = OrganDiseasesModel(
        organ="Heart",
        common_diseases=["CAD", "Heart Failure"],
        rare_diseases=["Brugada Syndrome"],
        educational_points=["Exercise daily", "Low salt diet"]
    )
    
    mock_output = ModelOutput(data=mock_data, markdown=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    result = generator.generate_text("Heart", structured=True)
    assert result.data.organ == "Heart"

@patch('medical.organ_diseases.organ_disease_info.save_model_response')
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = DiseaseInfoGenerator(config)
    mock_output = ModelOutput(markdown="Info")
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    generator.generate_text("Heart")
    generator.save(mock_output, Path("/tmp"))
    
    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("heart_diseases")
