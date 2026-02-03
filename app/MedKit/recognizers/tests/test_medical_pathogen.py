import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from medical_pathogen.recognizer import MedicalPathogenIdentifier
from medical_pathogen.models import ModelOutput, PathogenIdentifierModel, PathogenIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def pathogen_identifier(mock_model_config):
    with patch('medical_pathogen.recognizer.LiteClient'):
        return MedicalPathogenIdentifier(mock_model_config)

def test_identify(pathogen_identifier):
    # Setup mock response
    mock_data = PathogenIdentifierModel(
        identification=PathogenIdentificationModel(
            pathogen_name="Staphylococcus aureus",
            is_well_known=True,
            pathogen_type="Bacteria",
            associated_infections=["Skin infections", "Pneumonia", "Endocarditis"],
            clinical_significance="Common human pathogen; some strains are antibiotic-resistant (MRSA)."
        ),
        summary="S. aureus is a well-known bacterial pathogen.",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    
    pathogen_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = pathogen_identifier.identify("Staphylococcus aureus")
    
    # Assert
    assert result.data.identification.pathogen_name == "Staphylococcus aureus"
    assert result.data.identification.is_well_known is True
    assert pathogen_identifier.client.generate_text.called

def test_identify(pathogen_identifier):
    with pytest.raises(ValueError, match="Pathogen name cannot be empty"):
        pathogen_identifier.identify("")
