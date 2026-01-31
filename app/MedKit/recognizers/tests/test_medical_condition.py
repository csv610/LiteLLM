import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from medical_condition.recognizer import MedicalConditionIdentifier
from medical_condition.models import ModelOutput, MedicalConditionIdentifierModel, MedicalConditionIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def condition_identifier(mock_model_config):
    with patch('medical_condition.recognizer.LiteClient'):
        return MedicalConditionIdentifier(mock_model_config)

def test_identify_condition_success(condition_identifier):
    # Setup mock response
    mock_data = MedicalConditionIdentifierModel(
        identification=MedicalConditionIdentificationModel(
            condition_name="Hypertension",
            is_well_known=True,
            category="Chronic disease",
            key_characteristics=["High blood pressure", "Asymptomatic"],
            clinical_significance="Major risk factor for heart disease."
        ),
        summary="Hypertension is a well-known condition.",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    
    condition_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = condition_identifier.identify_condition("Hypertension")
    
    # Assert
    assert result.data.identification.condition_name == "Hypertension"
    assert result.data.identification.is_well_known is True
    assert condition_identifier.client.generate_text.called

def test_identify_condition_empty_name(condition_identifier):
    with pytest.raises(ValueError, match="Condition name cannot be empty"):
        condition_identifier.identify_condition("")

