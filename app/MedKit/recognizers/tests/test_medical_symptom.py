import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from medical_symptom.recognizer import MedicalSymptomIdentifier
from medical_symptom.models import ModelOutput, MedicalSymptomIdentifierModel, MedicalSymptomIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def symptom_identifier(mock_model_config):
    with patch('medical_symptom.recognizer.LiteClient'):
        return MedicalSymptomIdentifier(mock_model_config)

def test_identify(symptom_identifier):
    # Setup mock response
    mock_data = MedicalSymptomIdentifierModel(
        identification=MedicalSymptomIdentificationModel(
            symptom_name="Jaundice",
            is_well_known=True,
            associated_conditions=["Hepatitis", "Liver cirrhosis"],
            severity_indicators="Dark urine, pale stools, abdominal pain.",
            clinical_description="Yellowish pigmentation of the skin and eyes."
        ),
        summary="Jaundice is a well-known medical symptom.",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    
    symptom_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = symptom_identifier.identify("Jaundice")
    
    # Assert
    assert result.data.identification.symptom_name == "Jaundice"
    assert result.data.identification.is_well_known is True
    assert symptom_identifier.client.generate_text.called

def test_identify(symptom_identifier):
    with pytest.raises(ValueError, match="Symptom name cannot be empty"):
        symptom_identifier.identify("")

