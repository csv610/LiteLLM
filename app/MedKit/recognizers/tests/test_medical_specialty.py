import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from recognizers.medical_specialty.medical_specialty_identifier import MedicalSpecialtyIdentifier
from recognizers.medical_specialty.medical_specialty_models import ModelOutput, MedicalSpecialtyIdentifierModel, MedicalSpecialtyIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def specialty_identifier(mock_model_config):
    with patch('lite.lite_client.LiteClient'):
        id_obj = MedicalSpecialtyIdentifier(mock_model_config)
        id_obj.client.generate_text = MagicMock()
        return id_obj

def test_identify(specialty_identifier):
    # Setup mock response
    mock_data = MedicalSpecialtyIdentificationModel(
        name="Cardiology",
        description="Focuses on heart and vascular system",
        specialty_name="Cardiology",
        is_well_known=True,
        common_uses=["Heart health"],
        regulatory_status="N/A",
        industry_significance="Major specialty",
        scope_of_practice=["Heart and vessels"],
        training_requirements=["Internal medicine residency + Cardiology fellowship"],
        clinical_focus="Cardiovascular system",
        typical_procedures=["ECG", "ECHO"],
        related_specialties=["Cardiothoracic surgery"],
        board_certification_body="ABIM",
        related_orgs=["ACC", "AHA"],
        related_procedures=["Angioplasty"]
    )
    mock_model = MedicalSpecialtyIdentifierModel(identification=mock_data, summary="Specialty info", data_available=True)
    mock_output = ModelOutput(data=mock_model, data_available=True)
    specialty_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = specialty_identifier.identify("Cardiology")
    
    # Assert
    assert result.data.identification.specialty_name == "Cardiology"
    assert result.data.identification.is_well_known is True
    assert specialty_identifier.client.generate_text.called

def test_identify_empty_name(specialty_identifier):
    with pytest.raises(ValueError, match=".+"):
        specialty_identifier.identify("")
