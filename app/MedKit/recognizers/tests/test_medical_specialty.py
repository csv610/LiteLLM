import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from medical_specialty.recognizer import MedicalSpecialtyIdentifier
from medical_specialty.models import ModelOutput, MedicalSpecialtyIdentifierModel, MedicalSpecialtyIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def specialty_identifier(mock_model_config):
    with patch('medical_specialty.recognizer.LiteClient'):
        return MedicalSpecialtyIdentifier(mock_model_config)

def test_identify_specialty_success(specialty_identifier):
    # Setup mock response
    mock_data = MedicalSpecialtyIdentifierModel(
        identification=MedicalSpecialtyIdentificationModel(
            specialty_name="Cardiology",
            is_well_known=True,
            organs_treated=["Heart", "Blood vessels"],
            common_procedures=["EKG", "Angioplasty", "Echocardiogram"],
            clinical_scope="Diagnosis and treatment of heart and vascular disorders."
        ),
        summary="Cardiology is a well-known medical specialty.",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    
    specialty_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = specialty_identifier.identify_specialty("Cardiology")
    
    # Assert
    assert result.data.identification.specialty_name == "Cardiology"
    assert result.data.identification.is_well_known is True
    assert specialty_identifier.client.generate_text.called

def test_identify_specialty_empty_name(specialty_identifier):
    with pytest.raises(ValueError, match="Specialty name cannot be empty"):
        specialty_identifier.identify_specialty("")

