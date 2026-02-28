import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from recognizers.medical_vaccine.medical_vaccine_identifier import MedicalVaccineIdentifier
from recognizers.medical_vaccine.medical_vaccine_models import ModelOutput, VaccineIdentifierModel, VaccineIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def vaccine_identifier(mock_model_config):
    with patch('lite.lite_client.LiteClient'):
        id_obj = MedicalVaccineIdentifier(mock_model_config)
        id_obj.client.generate_text = MagicMock()
        return id_obj

def test_identify(vaccine_identifier):
    # Setup mock response
    mock_data = VaccineIdentificationModel(
        name="Influenza vaccine",
        description="Prevents seasonal flu",
        vaccine_name="Influenza",
        is_well_known=True,
        common_uses=["Prevention of flu"],
        regulatory_status="Approved",
        industry_significance="Common vaccine",
        vaccine_type="Inactivated",
        target_pathogen="Influenza virus",
        administration_route="Intramuscular",
        typical_schedule="Annual",
        safety_profile="Generally safe",
        contraindications=["Severe egg allergy"],
        manufacturer_info="Various"
    )
    mock_model = VaccineIdentifierModel(identification=mock_data, summary="Vaccine info", data_available=True)
    mock_output = ModelOutput(data=mock_model, data_available=True)
    
    vaccine_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = vaccine_identifier.identify("Influenza")
    
    # Assert
    assert result.data.identification.vaccine_name == "Influenza"
    assert result.data.identification.is_well_known is True
    assert vaccine_identifier.client.generate_text.called

def test_identify_empty_name(vaccine_identifier):
    with pytest.raises(ValueError, match=".+"):
        vaccine_identifier.identify("")
