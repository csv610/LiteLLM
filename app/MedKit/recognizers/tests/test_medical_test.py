import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from medical_test.recognizer import MedicalTestIdentifier
from medical_test.models import ModelOutput, MedicalTestIdentifierModel, MedicalTestIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def test_identifier(mock_model_config):
    with patch('medical_test.recognizer.LiteClient'):
        return MedicalTestIdentifier(mock_model_config)

def test_identify(test_identifier):
    # Setup mock response
    mock_data = MedicalTestIdentifierModel(
        identification=MedicalTestIdentificationModel(
            test_name="HbA1c",
            is_well_known=True,
            test_type="Blood test",
            purpose="Monitor long-term blood sugar levels",
            clinical_utility="Gold standard for diabetes management."
        ),
        summary="HbA1c is a well-known test.",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    
    test_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = test_identifier.identify("HbA1c")
    
    # Assert
    assert result.data.identification.test_name == "HbA1c"
    assert result.data.identification.is_well_known is True
    assert test_identifier.client.generate_text.called

def test_identify(test_identifier):
    with pytest.raises(ValueError, match="Test name cannot be empty"):
        test_identifier.identify("")

