import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)
from unittest.mock import MagicMock, patch

import pytest
from lite.config import ModelConfig

from ..medication_class.medication_class_models import (
    MedicationClassIdentificationModel,
    MedicationClassIdentifierModel,
    ModelOutput,
)
from ..medication_class.medication_class_recognizer import MedicationClassIdentifier


@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)


@pytest.fixture
def class_identifier(mock_model_config):
    with patch("lite.lite_client.LiteClient"):
        id_obj = MedicationClassIdentifier(mock_model_config)
        id_obj.client.generate_text = MagicMock()
        return id_obj


def test_identify(class_identifier):
    # Setup mock response
    mock_data = MedicationClassIdentificationModel(
        name="NSAIDs",
        description="Non-steroidal anti-inflammatory drugs",
        class_name="NSAIDs",
        is_well_known=True,
        common_uses=["Pain relief", "Anti-inflammatory"],
        regulatory_status="N/A",
        industry_significance="Common drug class",
        mechanism_of_action="COX inhibition",
        typical_drugs=["Aspirin", "Ibuprofen"],
        therapeutic_category="Analgesic",
        contraindications=["Peptic ulcer"],
        side_effects=["Gastric irritation"],
        safety_information="Take with food",
    )
    mock_model = MedicationClassIdentifierModel(
        identification=mock_data, summary="Class info", data_available=True
    )
    mock_output = ModelOutput(data=mock_model, data_available=True)

    class_identifier.client.generate_text.return_value = mock_output

    # Execute
    result = class_identifier.identify("NSAIDs")

    # Assert
    assert result.data.identification.class_name == "NSAIDs"
    assert result.data.identification.is_well_known is True
    assert class_identifier.client.generate_text.called


def test_identify_empty_name(class_identifier):
    with pytest.raises(ValueError, match=".+"):
        class_identifier.identify("")
