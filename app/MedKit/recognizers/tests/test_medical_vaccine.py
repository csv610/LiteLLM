import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from medical_vaccine.recognizer import MedicalVaccineIdentifier
from medical_vaccine.models import ModelOutput, VaccineIdentifierModel, VaccineIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def vaccine_identifier(mock_model_config):
    with patch('medical_vaccine.recognizer.LiteClient'):
        return MedicalVaccineIdentifier(mock_model_config)

def test_identify(vaccine_identifier):
    # Setup mock response
    mock_data = VaccineIdentifierModel(
        identification=VaccineIdentificationModel(
            vaccine_name="MMR",
            is_well_known=True,
            target_diseases=["Measles", "Mumps", "Rubella"],
            vaccine_type="Live-attenuated",
            standard_schedule="Two doses; 12-15 months and 4-6 years."
        ),
        summary="MMR is a standard childhood vaccine.",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    
    vaccine_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = vaccine_identifier.identify("MMR")
    
    # Assert
    assert result.data.identification.vaccine_name == "MMR"
    assert result.data.identification.is_well_known is True
    assert vaccine_identifier.client.generate_text.called

def test_identify(vaccine_identifier):
    with pytest.raises(ValueError, match="Vaccine name cannot be empty"):
        vaccine_identifier.identify("")
