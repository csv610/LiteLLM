import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from ..drug.drug_recognizer import DrugIdentifier
from ..drug.drug_recognizer_model import ModelOutput, DrugIdentifierModel, DrugIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def drug_identifier(mock_model_config):
    with patch('lite.lite_client.LiteClient') as mock_client:
        identifier = DrugIdentifier(mock_model_config)
        identifier.client.generate_text = MagicMock()
        return identifier

def test_identify(drug_identifier):
    # Setup mock response
    mock_data = DrugIdentifierModel(
        identification=DrugIdentificationModel(
            name="Aspirin",
            description="Common NSAID",
            drug_name="Aspirin",
            is_well_known=True,
            common_uses=["Pain relief", "Fever reduction"],
            regulatory_status="FDA approved",
            industry_significance="Extremely well-known and widely used.",
            mechanism_of_action="COX inhibitor",
            pharmacological_class="NSAID",
            drug_class="NSAID",
            regulatory_agency="FDA",
            legal_status="OTC"
        ),
        summary="Aspirin is a well-known drug.",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data, data_available=True)
    
    drug_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = drug_identifier.identify("Aspirin")
    
    # Assert
    assert result.data.identification.drug_name == "Aspirin"
    assert result.data.identification.is_well_known is True
    assert drug_identifier.client.generate_text.called

def test_identify_empty_name(drug_identifier):
    with pytest.raises(ValueError, match=".+"):
        drug_identifier.identify("")
