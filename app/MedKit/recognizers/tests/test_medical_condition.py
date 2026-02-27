import sys
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from ..medical_condition.medical_condition_identifier import MedicalConditionIdentifier
from ..medical_condition.medical_condition_models import ModelOutput, MedicalConditionIdentifierModel, MedicalConditionIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def condition_identifier(mock_model_config):
    with patch('lite.lite_client.LiteClient'):
        id_obj = MedicalConditionIdentifier(mock_model_config)
        id_obj.client.generate_text = MagicMock()
        return id_obj

def test_identify(condition_identifier):
    # Setup mock response
    mock_data = MedicalConditionIdentificationModel(
        name="Diabetes",
        description="Chronic metabolic disorder",
        condition_name="Diabetes",
        is_well_known=True,
        common_uses=["N/A"],
        regulatory_status="N/A",
        industry_significance="Chronic disease",
        typical_symptoms=["Thirst"],
        common_treatments=["Insulin"],
        clinical_relevance="Requires lifelong management",
        risk_profile="High complications if untreated",
        differential_diagnosis=["Type 1 vs Type 2"],
        prognosis="Good with management"
    )
    mock_model = MedicalConditionIdentifierModel(identification=mock_data, summary="Condition info", data_available=True)
    mock_output = ModelOutput(data=mock_model, data_available=True)
    
    condition_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = condition_identifier.identify("Diabetes")
    
    # Assert
    assert result.data.identification.condition_name == "Diabetes"
    assert result.data.identification.is_well_known is True
    assert condition_identifier.client.generate_text.called

def test_identify_empty_name(condition_identifier):
    with pytest.raises(ValueError, match=".+"):
        condition_identifier.identify("")
