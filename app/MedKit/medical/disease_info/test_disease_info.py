import pytest
from unittest.mock import MagicMock, patch
from disease_info import DiseaseInfoGenerator
from lite.config import ModelConfig, ModelOutput
from disease_info_models import DiseaseInfoModel

@pytest.fixture
def mock_lite_client():
    with patch('disease_info.LiteClient') as mock:
        yield mock

def test_disease_info_generator_init():
    config = ModelConfig(model="test-model")
    generator = DiseaseInfoGenerator(config)
    assert generator.model_config == config
    assert generator.client is not None

def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = DiseaseInfoGenerator(config)
    
    mock_client_instance = mock_lite_client.return_value
    mock_client_instance.generate_text.return_value = "Disease info in markdown"
    
    output = generator.generate_text(disease="Flu", structured=False)
    
    assert output.markdown == "Disease info in markdown"
    assert output.data is None
    mock_client_instance.generate_text.assert_called_once()

def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = DiseaseInfoGenerator(config)
    
    # Minimal mock data for structured output
    mock_data = MagicMock(spec=DiseaseInfoModel)
    
    mock_client_instance = mock_lite_client.return_value
    mock_client_instance.generate_text.return_value = mock_data
    
    output = generator.generate_text(disease="Flu", structured=True)
    
    assert output.data == mock_data
    assert output.markdown is None
    mock_client_instance.generate_text.assert_called_once()
