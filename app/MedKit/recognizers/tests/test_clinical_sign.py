import pytest
from unittest.mock import MagicMock, patch
from clinical_sign.recognizer import ClinicalSignIdentifier
from clinical_sign.models import ModelOutput, ClinicalSignIdentifierModel, ClinicalSignIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def sign_identifier(mock_model_config):
    with patch('clinical_sign.recognizer.LiteClient'):
        return ClinicalSignIdentifier(mock_model_config)

def test_identify_sign_success(sign_identifier):
    mock_data = ClinicalSignIdentifierModel(
        identification=ClinicalSignIdentificationModel(
            sign_name="Babinski sign",
            is_well_known=True,
            examination_method="Stroking the sole of the foot",
            clinical_significance="Upper motor neuron lesion"
        ),
        summary="Summary",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    sign_identifier.client.generate_text.return_value = mock_output
    result = sign_identifier.identify_sign("Babinski")
    assert result.data.identification.sign_name == "Babinski sign"
