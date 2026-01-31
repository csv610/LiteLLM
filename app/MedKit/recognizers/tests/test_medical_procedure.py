import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from medical_procedure.recognizer import MedicalProcedureIdentifier
from medical_procedure.models import ModelOutput, MedicalProcedureIdentifierModel, MedicalProcedureIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def procedure_identifier(mock_model_config):
    with patch('medical_procedure.recognizer.LiteClient'):
        return MedicalProcedureIdentifier(mock_model_config)

def test_identify_procedure_success(procedure_identifier):
    # Setup mock response
    mock_data = MedicalProcedureIdentifierModel(
        identification=MedicalProcedureIdentificationModel(
            procedure_name="Appendectomy",
            is_well_known=True,
            procedure_type="Surgical intervention",
            indications=["Acute appendicitis"],
            clinical_significance="Standard emergency surgery to remove the appendix."
        ),
        summary="Appendectomy is a well-known medical procedure.",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    
    procedure_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = procedure_identifier.identify_procedure("Appendectomy")
    
    # Assert
    assert result.data.identification.procedure_name == "Appendectomy"
    assert result.data.identification.is_well_known is True
    assert procedure_identifier.client.generate_text.called

def test_identify_procedure_empty_name(procedure_identifier):
    with pytest.raises(ValueError, match="Procedure name cannot be empty"):
        procedure_identifier.identify_procedure("")

