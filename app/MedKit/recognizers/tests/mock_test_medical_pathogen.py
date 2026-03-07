import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from ..medical_pathogen.medical_pathogen_identifier import MedicalPathogenIdentifier
from ..medical_pathogen.medical_pathogen_models import ModelOutput, PathogenIdentifierModel, PathogenIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def pathogen_identifier(mock_model_config):
    with patch('lite.lite_client.LiteClient'):
        id_obj = MedicalPathogenIdentifier(mock_model_config)
        id_obj.client.generate_text = MagicMock()
        return id_obj

def test_identify(pathogen_identifier):
    # Setup mock response
    mock_data = PathogenIdentificationModel(
        name="E. coli",
        description="Common gram-negative bacterium",
        pathogen_name="E. coli",
        is_well_known=True,
        common_uses=["N/A"],
        regulatory_status="N/A",
        industry_significance="Common bacterium",
        pathogen_type="Bacterium",
        typical_infections=["UTI"],
        transmission_modes=["Fecal-oral"],
        clinical_relevance="Common cause of UTI",
        diagnostic_methods=["Culture", "PCR"],
        resistance_patterns=["ESBL possible"]
    )
    mock_model = PathogenIdentifierModel(identification=mock_data, summary="Pathogen info", data_available=True)
    mock_output = ModelOutput(data=mock_model, data_available=True)
    pathogen_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = pathogen_identifier.identify("E. coli")
    
    # Assert
    assert result.data.identification.pathogen_name == "E. coli"
    assert result.data.identification.is_well_known is True
    assert pathogen_identifier.client.generate_text.called

def test_identify_empty_name(pathogen_identifier):
    with pytest.raises(ValueError, match=".+"):
        pathogen_identifier.identify("")
