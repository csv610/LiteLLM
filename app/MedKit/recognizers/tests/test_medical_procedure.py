import sys
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from ..medical_procedure.medical_procedure_identifier import MedicalProcedureIdentifier
from ..medical_procedure.medical_procedure_models import ModelOutput, MedicalProcedureIdentifierModel, MedicalProcedureIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def procedure_identifier(mock_model_config):
    with patch('lite.lite_client.LiteClient'):
        id_obj = MedicalProcedureIdentifier(mock_model_config)
        id_obj.client.generate_text = MagicMock()
        return id_obj

def test_identify(procedure_identifier):
    # Setup mock response
    mock_data = MedicalProcedureIdentificationModel(
        name="Appendectomy",
        description="Surgical removal of appendix",
        procedure_name="Appendectomy",
        is_well_known=True,
        common_uses=["Removing appendix"],
        regulatory_status="Standard procedure",
        industry_significance="Common surgery",
        procedure_type="Surgery",
        typical_indications=["Appendicitis"],
        procedure_category="Emergency",
        typical_duration="1 hour",
        risk_profile="Moderate",
        clinical_outcome_expectations="Full recovery",
        equipment_required=["Laparoscope"],
        aftercare_requirements=["Rest", "Antibiotics"]
    )
    mock_model = MedicalProcedureIdentifierModel(identification=mock_data, summary="Procedure info", data_available=True)
    mock_output = ModelOutput(data=mock_model, data_available=True)
    procedure_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = procedure_identifier.identify("Appendectomy")
    
    # Assert
    assert result.data.identification.procedure_name == "Appendectomy"
    assert result.data.identification.is_well_known is True
    assert procedure_identifier.client.generate_text.called

def test_identify_empty_name(procedure_identifier):
    with pytest.raises(ValueError, match=".+"):
        procedure_identifier.identify("")
