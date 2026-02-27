import sys
from pathlib import Path
import pytest
from unittest.mock import patch

from ..disease.disease_recognizer import DiseaseIdentifier
from ..disease.disease_identifier_models import ModelOutput, DiseaseIdentifierModel, DiseaseIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def identifier(mock_model_config):
    with patch('lite.lite_client.LiteClient'):
        return DiseaseIdentifier(mock_model_config)

def test_identify(identifier):
    mock_data = DiseaseIdentifierModel(
        identification=DiseaseIdentificationModel(
            name="Asthma",
            description="Chronic respiratory condition",
            disease_name="Asthma",
            is_well_known=True,
            common_uses=["N/A"],
            regulatory_status="N/A",
            industry_significance="Common condition",
            prevalence="High",
            severity="Variable",
            typical_symptoms=["Wheezing"],
            common_treatments=["Inhalers"]
        ),
        summary="Asthma is a common condition.",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data, data_available=True)
    identifier.client.generate_text.return_value = mock_output
    
    result = identifier.identify("Asthma")
    assert result.data.identification.disease_name == "Asthma"
    assert result.data.identification.is_well_known is True
