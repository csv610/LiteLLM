import pytest
from unittest.mock import MagicMock, patch
from medical_faq import MedicalFAQGenerator
from lite.config import ModelConfig, ModelOutput
from medical_faq_models import MedicalFAQModel

@pytest.fixture
def mock_lite_client():
    with patch('medical_faq.LiteClient') as mock:
        yield mock

def test_medical_faq_generator_init():
    config = ModelConfig(model="test-model")
    generator = MedicalFAQGenerator(config)
    assert generator.model_config == config
    assert generator.client is not None

def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalFAQGenerator(config)
    
    mock_client_instance = mock_lite_client.return_value
    mock_client_instance.generate_text.return_value = "FAQ in markdown"
    
    output = generator.generate_text(topic="Diabetes", structured=False)
    
    assert output.markdown == "FAQ in markdown"
    assert output.data is None
    mock_client_instance.generate_text.assert_called_once()

def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalFAQGenerator(config)
    
    mock_data = MagicMock(spec=MedicalFAQModel)
    
    mock_client_instance = mock_lite_client.return_value
    mock_client_instance.generate_text.return_value = mock_data
    
    output = generator.generate_text(topic="Diabetes", structured=True)
    
    assert output.data == mock_data
    assert output.markdown is None
    mock_client_instance.generate_text.assert_called_once()
