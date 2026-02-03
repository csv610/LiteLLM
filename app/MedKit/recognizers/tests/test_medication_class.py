import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from medication_class.recognizer import MedicationClassIdentifier
from medication_class.models import ModelOutput, MedicationClassIdentifierModel, MedicationClassIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def class_identifier(mock_model_config):
    with patch('medication_class.recognizer.LiteClient'):
        return MedicationClassIdentifier(mock_model_config)

def test_identify(class_identifier):
    # Setup mock response
    mock_data = MedicationClassIdentifierModel(
        identification=MedicationClassIdentificationModel(
            class_name="SSRIs",
            is_well_known=True,
            mechanism_of_action="Inhibit reuptake of serotonin",
            common_examples=["Fluoxetine", "Sertraline"],
            therapeutic_uses=["Depression", "Anxiety"]
        ),
        summary="SSRIs are a standard class of antidepressants.",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    
    class_identifier.client.generate_text.return_value = mock_output
    
    # Execute
    result = class_identifier.identify("SSRIs")
    
    # Assert
    assert result.data.identification.class_name == "SSRIs"
    assert result.data.identification.is_well_known is True
    assert class_identifier.client.generate_text.called

def test_identify(class_identifier):
    with pytest.raises(ValueError, match="Class name cannot be empty"):
        class_identifier.identify("")
