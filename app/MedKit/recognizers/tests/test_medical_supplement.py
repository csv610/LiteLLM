import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from medical_supplement.recognizer import MedicalSupplementIdentifier
from medical_supplement.models import ModelOutput, SupplementIdentifierModel, SupplementIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def supplement_identifier(mock_model_config):
    with patch('medical_supplement.recognizer.LiteClient'):
        return MedicalSupplementIdentifier(mock_model_config)

def test_identify(supplement_identifier):
    # Setup mock response
    mock_data = SupplementIdentifierModel(
        identification=SupplementIdentificationModel(
            supplement_name="Vitamin D3",
            is_well_known=True,
            primary_nutrients=["Cholecalciferol"],
            common_uses=["Bone health", "Immune support"],
            regulatory_standing="Regulated as a dietary supplement by the FDA."
        ),
        summary="Vitamin D3 is a common nutritional supplement.",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    
    supplement_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = supplement_identifier.identify("Vitamin D3")
    
    # Assert
    assert result.data.identification.supplement_name == "Vitamin D3"
    assert result.data.identification.is_well_known is True
    assert supplement_identifier.client.generate_text.called

def test_identify(supplement_identifier):
    with pytest.raises(ValueError, match="Supplement name cannot be empty"):
        supplement_identifier.identify("")
