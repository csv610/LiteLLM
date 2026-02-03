import pytest
from unittest.mock import MagicMock, patch
from lab_unit.recognizer import LabUnitIdentifier
from lab_unit.models import ModelOutput, LabUnitIdentifierModel, LabUnitIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def identifier(mock_model_config):
    with patch('lab_unit.recognizer.LiteClient'):
        return LabUnitIdentifier(mock_model_config)

def test_identify(identifier):
    mock_data = LabUnitIdentifierModel(
        identification=LabUnitIdentificationModel(
            unit_name="mEq/L",
            is_well_known=True,
            category='Concentration', common_tests=['Electrolytes']
        ),
        summary="Summary",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    identifier.client.generate_text.return_value = mock_output
    result = identifier.identify("mEq/L")
    assert getattr(result.data.identification, 'unit_name') == "mEq/L"
