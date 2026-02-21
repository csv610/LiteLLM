import pytest
from unittest.mock import MagicMock, patch
from primary_health_care import PrimaryHealthCareProvider
from lite.config import ModelConfig, ModelInput, ModelOutput
from primary_health_care_models import PrimaryCareResponseModel

@pytest.fixture
def mock_lite_client():
    with patch('primary_health_care.LiteClient') as mock:
        yield mock

def test_primary_health_care_provider_init():
    config = ModelConfig(model="test-model")
    provider = PrimaryHealthCareProvider(config)
    assert provider.model_config == config
    assert provider.client is not None

def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    provider = PrimaryHealthCareProvider(config)
    
    mock_client_instance = mock_lite_client.return_value
    mock_client_instance.generate_text.return_value = "Test markdown response"
    
    output = provider.generate_text(query="I have a headache", structured=False)
    
    assert output.markdown == "Test markdown response"
    assert output.data is None
    mock_client_instance.generate_text.assert_called_once()

def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    provider = PrimaryHealthCareProvider(config)
    
    mock_data = PrimaryCareResponseModel(
        understanding_concern="Patient has a headache",
        common_symptoms=["Ache", "Pain"],
        general_explanation="Common condition",
        self_care_advice="Rest",
        when_to_seek_care="If persistent",
        next_steps=["See doctor"]
    )
    
    mock_client_instance = mock_lite_client.return_value
    mock_client_instance.generate_text.return_value = mock_data
    
    output = provider.generate_text(query="I have a headache", structured=True)
    
    assert output.data == mock_data
    assert output.markdown is None
    mock_client_instance.generate_text.assert_called_once()

def test_generate_text_empty_query():
    config = ModelConfig(model="test-model")
    provider = PrimaryHealthCareProvider(config)
    
    with pytest.raises(ValueError, match="Query cannot be empty"):
        provider.generate_text(query="")
