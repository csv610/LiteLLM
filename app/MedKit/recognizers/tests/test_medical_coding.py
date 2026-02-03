import pytest
from unittest.mock import MagicMock, patch
from medical_coding.recognizer import MedicalCodingIdentifier
from medical_coding.models import ModelOutput, MedicalCodingIdentifierModel, MedicalCodingIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def identifier(mock_model_config):
    with patch('medical_coding.recognizer.LiteClient'):
        return MedicalCodingIdentifier(mock_model_config)

def test_identify(identifier):
    mock_data = MedicalCodingIdentifierModel(
        identification=MedicalCodingIdentificationModel(
            system_name="ICD-10",
            is_well_known=True,
            purpose='Diagnosis coding', governing_body='WHO'
        ),
        summary="Summary",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    identifier.client.generate_text.return_value = mock_output
    result = identifier.identify("ICD-10")
    assert getattr(result.data.identification, 'system_name') == "ICD-10"
