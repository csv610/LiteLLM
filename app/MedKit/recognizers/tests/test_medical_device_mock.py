import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)
from unittest.mock import MagicMock, patch

import pytest
from lite.config import ModelConfig

from ..medical_device.medical_device_identifier import MedicalDeviceIdentifier
from ..medical_device.medical_device_models import (
    MedicalDeviceIdentificationModel,
    MedicalDeviceIdentifierModel,
    ModelOutput,
)


@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)


@pytest.fixture
def device_identifier(mock_model_config):
    with patch("lite.lite_client.LiteClient"):
        id_obj = MedicalDeviceIdentifier(mock_model_config)
        id_obj.client.generate_text = MagicMock()
        return id_obj


def test_identify(device_identifier):
    # Setup mock response
    mock_data = MedicalDeviceIdentificationModel(
        name="Pacemaker",
        description="Cardiac rhythm device",
        device_name="Pacemaker",
        is_well_known=True,
        common_uses=["Regulating heart rhythm"],
        regulatory_status="FDA approved",
        industry_significance="Life-saving device",
        device_class="Class III",
        manufacturer="Generic",
        clinical_indications=["Bradycardia"],
        safety_warnings=["Magnetic interference"],
        regulatory_approvals=["FDA", "CE"],
        maintenance_requirements=["Regular battery checks"],
    )
    mock_model = MedicalDeviceIdentifierModel(
        identification=mock_data, summary="Device info", data_available=True
    )
    mock_output = ModelOutput(data=mock_model, data_available=True)

    device_identifier.client.generate_text.return_value = mock_output

    # Execute
    result = device_identifier.identify("Pacemaker")

    # Assert
    assert result.data.identification.device_name == "Pacemaker"
    assert result.data.identification.is_well_known is True
    assert device_identifier.client.generate_text.called


def test_identify_empty_name(device_identifier):
    with pytest.raises(ValueError, match=".+"):
        device_identifier.identify("")
