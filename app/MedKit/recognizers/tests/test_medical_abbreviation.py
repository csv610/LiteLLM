import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from medical_abbreviation.recognizer import MedicalAbbreviationIdentifier
from medical_abbreviation.models import ModelOutput, AbbreviationIdentifierModel, AbbreviationIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def abbr_identifier(mock_model_config):
    with patch('medical_abbreviation.recognizer.LiteClient'):
        return MedicalAbbreviationIdentifier(mock_model_config)

def test_identify(abbr_identifier):
    # Setup mock response
    mock_data = AbbreviationIdentifierModel(
        identification=AbbreviationIdentificationModel(
            abbreviation="PRN",
            full_form="Pro Re Nata",
            is_well_known=True,
            context_of_use="Prescriptions",
            clinical_meaning="As needed"
        ),
        summary="PRN is a standard medical abbreviation.",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    
    abbr_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = abbr_identifier.identify("PRN")
    
    # Assert
    assert result.data.identification.abbreviation == "PRN"
    assert result.data.identification.is_well_known is True
    assert abbr_identifier.client.generate_text.called

def test_identify(abbr_identifier):
    with pytest.raises(ValueError, match="Abbreviation cannot be empty"):
        abbr_identifier.identify("")
