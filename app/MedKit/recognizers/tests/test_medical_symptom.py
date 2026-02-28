import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from recognizers.medical_symptom.medical_symptom_identifier import MedicalSymptomIdentifier
from recognizers.medical_symptom.medical_symptom_models import ModelOutput, MedicalSymptomIdentifierModel, MedicalSymptomIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def symptom_identifier(mock_model_config):
    with patch('lite.lite_client.LiteClient'):
        id_obj = MedicalSymptomIdentifier(mock_model_config)
        id_obj.client.generate_text = MagicMock()
        return id_obj

def test_identify(symptom_identifier):
    # Setup mock response
    mock_data = MedicalSymptomIdentificationModel(
        name="Chest pain",
        description="Pain or discomfort in the chest area",
        symptom_name="Chest pain",
        is_well_known=True,
        common_uses=["N/A"],
        regulatory_status="N/A",
        industry_significance="Common symptom",
        typical_causes=["Heart attack", "Muscle strain"],
        severity_levels=["Mild", "Severe"],
        clinical_relevance="Requires evaluation",
        duration_characteristics="Acute or chronic",
        associated_signs=["Sweating"],
        when_to_seek_help="Immediately if severe"
    )
    mock_model = MedicalSymptomIdentifierModel(identification=mock_data, summary="Symptom info", data_available=True)
    mock_output = ModelOutput(data=mock_model, data_available=True)
    symptom_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = symptom_identifier.identify("Chest pain")
    
    # Assert
    assert result.data.identification.symptom_name == "Chest pain"
    assert result.data.identification.is_well_known is True
    assert symptom_identifier.client.generate_text.called

def test_identify_empty_name(symptom_identifier):
    with pytest.raises(ValueError, match=".+"):
        symptom_identifier.identify("")
