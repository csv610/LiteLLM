import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from medical_anatomy.recognizer import MedicalAnatomyIdentifier
from medical_anatomy.models import ModelOutput, MedicalAnatomyIdentifierModel, MedicalAnatomyIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def anatomy_identifier(mock_model_config):
    with patch('medical_anatomy.recognizer.LiteClient'):
        return MedicalAnatomyIdentifier(mock_model_config)

def test_identify(anatomy_identifier):
    # Setup mock response
    mock_data = MedicalAnatomyIdentifierModel(
        identification=MedicalAnatomyIdentificationModel(
            structure_name="Heart",
            is_well_known=True,
            system="Cardiovascular system",
            location="Thoracic cavity",
            clinical_significance="Primary organ for pumping blood throughout the body."
        ),
        summary="The heart is a well-known anatomical structure.",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    
    anatomy_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = anatomy_identifier.identify("Heart")
    
    # Assert
    assert result.data.identification.structure_name == "Heart"
    assert result.data.identification.is_well_known is True
    assert anatomy_identifier.client.generate_text.called

def test_identify(anatomy_identifier):
    with pytest.raises(ValueError, match="Structure name cannot be empty"):
        anatomy_identifier.identify("")

