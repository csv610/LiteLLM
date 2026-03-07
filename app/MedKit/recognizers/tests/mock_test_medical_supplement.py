import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from recognizers.medical_supplement.medical_supplement_identifier import MedicalSupplementIdentifier
from recognizers.medical_supplement.medical_supplement_models import ModelOutput, SupplementIdentifierModel, SupplementIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def supplement_identifier(mock_model_config):
    with patch('lite.lite_client.LiteClient'):
        id_obj = MedicalSupplementIdentifier(mock_model_config)
        id_obj.client.generate_text = MagicMock()
        return id_obj

def test_identify(supplement_identifier):
    # Setup mock response
    mock_data = SupplementIdentificationModel(
        name="Vitamin D",
        description="Essential fat-soluble vitamin",
        supplement_name="Vitamin D",
        is_well_known=True,
        common_uses=["Bone health"],
        regulatory_status="Dietary supplement",
        industry_significance="Common supplement",
        typical_dosage="1000-2000 IU",
        safety_profile="Safe within limits",
        source_origin="Natural/Synthetic",
        common_forms=["Capsule", "Drops"],
        mechanism_of_action="Calcium absorption",
        potential_interactions=["Steroids"],
        dosage_instructions="Take with food"
    )
    mock_model = SupplementIdentifierModel(identification=mock_data, summary="Supplement info", data_available=True)
    mock_output = ModelOutput(data=mock_model, data_available=True)
    supplement_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = supplement_identifier.identify("Vitamin D")
    
    # Assert
    assert result.data.identification.supplement_name == "Vitamin D"
    assert result.data.identification.is_well_known is True
    assert supplement_identifier.client.generate_text.called

def test_identify_empty_name(supplement_identifier):
    with pytest.raises(ValueError, match=".+"):
        supplement_identifier.identify("")
