import pytest
from unittest.mock import MagicMock, patch
from med_ethics import MedEthicalQA
from lite.config import ModelConfig
from med_ethics_models import EthicalAnalysisModel, ModelOutput

@pytest.fixture
def mock_lite_client():
    # Make sure we're mocking the class correctly in its module
    with patch('med_ethics.LiteClient') as mock:
        yield mock

def test_med_ethical_qa_init():
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)
    assert generator.model_config == config
    assert generator.client is not None

def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)
    
    mock_client_instance = mock_lite_client.return_value
    mock_output = ModelOutput(markdown="Ethics analysis in markdown")
    mock_client_instance.generate_text.return_value = mock_output
    
    output = generator.generate_text(question="Is it ethical to use AI in medicine?", structured=False)
    
    assert output.markdown == "Ethics analysis in markdown"
    assert output.data is None
    mock_client_instance.generate_text.assert_called_once()

def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)
    
    # Minimal mock data for structured output
    mock_data = MagicMock(spec=EthicalAnalysisModel)
    mock_output = ModelOutput(data=mock_data)
    
    mock_client_instance = mock_lite_client.return_value
    mock_client_instance.generate_text.return_value = mock_output
    
    output = generator.generate_text(question="Is it ethical to use AI in medicine?", structured=True)
    
    assert output.data == mock_data
    assert output.markdown is None
    mock_client_instance.generate_text.assert_called_once()
