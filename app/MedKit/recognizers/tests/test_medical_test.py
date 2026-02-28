import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from recognizers.medical_test.medical_test_identifier import MedicalTestIdentifier
from recognizers.medical_test.medical_test_models import ModelOutput, MedicalTestIdentifierModel, MedicalTestIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def test_identifier(mock_model_config):
    with patch('lite.lite_client.LiteClient'):
        id_obj = MedicalTestIdentifier(mock_model_config)
        id_obj.client.generate_text = MagicMock()
        return id_obj

def test_identify(test_identifier):
    # Setup mock response
    mock_data = MedicalTestIdentificationModel(
        name="CBC",
        description="Complete blood count test",
        test_name="CBC",
        is_well_known=True,
        common_uses=["Checking blood counts"],
        regulatory_status="Standard test",
        industry_significance="Common lab test",
        specimen_type="Blood",
        normal_range="Variable",
        test_category="Hematology",
        typical_turnaround_time="24 hours",
        clinical_utility="General health check",
        diagnostic_accuracy="High",
        related_tests=["BMP"],
        limitations_of_test=["N/A"]
    )
    mock_model = MedicalTestIdentifierModel(identification=mock_data, summary="Test info", data_available=True)
    mock_output = ModelOutput(data=mock_model, data_available=True)
    
    test_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = test_identifier.identify("CBC")
    
    # Assert
    assert result.data.identification.test_name == "CBC"
    assert result.data.identification.is_well_known is True
    assert test_identifier.client.generate_text.called

def test_identify_empty_name(test_identifier):
    with pytest.raises(ValueError, match=".+"):
        test_identifier.identify("")
