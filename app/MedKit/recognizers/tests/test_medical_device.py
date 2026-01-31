import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from medical_device.recognizer import MedicalDeviceIdentifier
from medical_device.models import ModelOutput, MedicalDeviceIdentifierModel, MedicalDeviceIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def device_identifier(mock_model_config):
    with patch('medical_device.recognizer.LiteClient'):
        return MedicalDeviceIdentifier(mock_model_config)

def test_identify_device_success(device_identifier):
    # Setup mock response
    mock_data = MedicalDeviceIdentifierModel(
        identification=MedicalDeviceIdentificationModel(
            device_name="Pacemaker",
            is_well_known=True,
            device_category="Implantable therapeutic device",
            primary_function="Regulate heart rhythm",
            clinical_significance="Life-saving device for cardiac patients."
        ),
        summary="Pacemaker is a well-known medical device.",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    
    device_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = device_identifier.identify_device("Pacemaker")
    
    # Assert
    assert result.data.identification.device_name == "Pacemaker"
    assert result.data.identification.is_well_known is True
    assert device_identifier.client.generate_text.called

def test_identify_device_empty_name(device_identifier):
    with pytest.raises(ValueError, match="Device name cannot be empty"):
        device_identifier.identify_device("")

