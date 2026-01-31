import pytest
from unittest.mock import MagicMock, patch
from imaging_finding.recognizer import ImagingFindingIdentifier
from imaging_finding.models import ModelOutput, ImagingFindingIdentifierModel, ImagingFindingIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def identifier(mock_model_config):
    with patch('imaging_finding.recognizer.LiteClient'):
        return ImagingFindingIdentifier(mock_model_config)

def test_identify_success(identifier):
    mock_data = ImagingFindingIdentifierModel(
        identification=ImagingFindingIdentificationModel(
            finding_name="Consolidation",
            is_well_known=True,
            modalities=['CT'], differential_diagnosis=['Pneumonia']
        ),
        summary="Summary",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    identifier.client.generate_text.return_value = mock_output
    result = identifier.identify_finding("Consolidation")
    assert getattr(result.data.identification, 'finding_name') == "Consolidation"
