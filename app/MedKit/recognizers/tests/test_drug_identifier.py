import pytest
from unittest.mock import MagicMock, patch
from drug.recognizer import DrugIdentifier
from drug.models import ModelOutput, DrugIdentifierModel, DrugIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def drug_identifier(mock_model_config):
    with patch('drug.recognizer.LiteClient'):
        return DrugIdentifier(mock_model_config)

def test_identify_drug_success(drug_identifier):
    # Setup mock response
    mock_data = DrugIdentifierModel(
        identification=DrugIdentificationModel(
            drug_name="Aspirin",
            is_well_known=True,
            common_uses=["Pain relief", "Fever reduction"],
            regulatory_status="FDA approved",
            industry_significance="Extremely well-known and widely used."
        ),
        summary="Aspirin is a well-known drug.",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    
    drug_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = drug_identifier.identify_drug("Aspirin")
    
    # Assert
    assert result.data.identification.drug_name == "Aspirin"
    assert result.data.identification.is_well_known is True
    assert drug_identifier.client.generate_text.called

def test_identify_drug_empty_name(drug_identifier):
    with pytest.raises(ValueError, match="Drug name cannot be empty"):
        drug_identifier.identify_drug("")