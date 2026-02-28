import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from unittest.mock import patch
from medical.med_advise.primary_health_care import PrimaryHealthCareProvider
from lite.config import ModelConfig
from medical.med_advise.primary_health_care_models import PrimaryCareResponseModel, ModelOutput

@pytest.fixture
def mock_lite_client():
    with patch('medical.med_advise.primary_health_care.LiteClient') as mock:
        yield mock

def test_primary_health_care_provider_init():
    config = ModelConfig(model="test-model")
    provider = PrimaryHealthCareProvider(config)
    assert provider.model_config == config

def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    provider = PrimaryHealthCareProvider(config)
    mock_output = ModelOutput(markdown="Primary care advice", data_available=True)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    result = provider.generate_text("I have a cough")
    assert result.markdown == "Primary care advice"

def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    provider = PrimaryHealthCareProvider(config)
    mock_data = PrimaryCareResponseModel(
        understanding_concern="Cough",
        common_symptoms=["Cough", "Fever"],
        general_explanation="A chronic cough",
        self_care_advice="Rest",
        when_to_seek_care="Fever",
        next_steps=["See doctor"]
    )
    mock_output = ModelOutput(data=mock_data, data_available=True)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    result = provider.generate_text("I have a cough", structured=True)
    assert result.data.understanding_concern == "Cough"
