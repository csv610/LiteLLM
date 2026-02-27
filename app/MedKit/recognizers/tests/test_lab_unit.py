import sys
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from ..lab_unit.lab_unit_recognizer import LabUnitIdentifier
from ..lab_unit.lab_unit_models import ModelOutput, LabUnitIdentifierModel, LabUnitIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def identifier(mock_model_config):
    with patch('lite.lite_client.LiteClient'):
        id_obj = LabUnitIdentifier(mock_model_config)
        id_obj.client.generate_text = MagicMock()
        return id_obj

def test_identify(identifier):
    mock_data = LabUnitIdentificationModel(
        name="mg/dL",
        description="Common lab unit",
        unit_name="mg/dL",
        is_well_known=True,
        common_uses=["Laboratory measurement"],
        regulatory_status="Standard unit",
        industry_significance="Common lab unit",
        system_of_measurement="Metric",
        measured_property="Concentration",
        common_abbreviations=["mg/dL"],
        si_equivalent="mg/dL"
    )
    mock_model = LabUnitIdentifierModel(identification=mock_data, summary="Unit info", data_available=True)
    mock_output = ModelOutput(data=mock_model, data_available=True)
    identifier.client.generate_text.return_value = mock_output
    
    result = identifier.identify("mg/dL")
    assert result.data.identification.unit_name == "mg/dL"
    assert result.data.identification.is_well_known is True
