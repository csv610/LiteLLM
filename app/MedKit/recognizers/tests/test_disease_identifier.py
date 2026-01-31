import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from disease.recognizer import DiseaseIdentifier
from disease.models import ModelOutput, DiseaseIdentifierModel, DiseaseIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def disease_identifier(mock_model_config):
    with patch('disease.recognizer.LiteClient'):
        return DiseaseIdentifier(mock_model_config)

def test_identify_disease_success(disease_identifier):
    # Setup mock response
    mock_data = DiseaseIdentifierModel(
        identification=DiseaseIdentificationModel(
            disease_name="Diabetes",
            is_well_known=True,
            common_symptoms=["Thirst", "Frequent urination"],
            prevalence="Common",
            medical_significance="Significant chronic condition."
        ),
        summary="Diabetes is a well-known disease.",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    
    disease_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = disease_identifier.identify_disease("Diabetes")
    
    # Assert
    assert result.data.identification.disease_name == "Diabetes"
    assert result.data.identification.is_well_known is True
    assert disease_identifier.client.generate_text.called

def test_identify_disease_empty_name(disease_identifier):
    with pytest.raises(ValueError, match="Disease name cannot be empty"):
        disease_identifier.identify_disease("")

