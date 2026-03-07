import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)
from unittest.mock import MagicMock, patch

import pytest
from lite.config import ModelConfig

from ..medical_anatomy.medical_anatomy_identifier import MedicalAnatomyIdentifier
from ..medical_anatomy.medical_anatomy_identifier_models import (
    MedicalAnatomyIdentificationModel,
    MedicalAnatomyIdentifierModel,
    ModelOutput,
)


@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)


@pytest.fixture
def anatomy_identifier(mock_model_config):
    with patch("lite.lite_client.LiteClient"):
        id_obj = MedicalAnatomyIdentifier(mock_model_config)
        id_obj.client.generate_text = MagicMock()
        return id_obj


def test_identify(anatomy_identifier):
    # Setup mock response
    mock_data = MedicalAnatomyIdentificationModel(
        name="Heart",
        description="Vital cardiovascular organ",
        structure_name="Heart",
        is_well_known=True,
        common_uses=["Pumping blood"],
        regulatory_status="N/A",
        industry_significance="Vital organ",
        system="Cardiovascular",
        location="Chest",
        clinical_relevance="Key for life",
        function="Pumping blood",
        blood_supply="Coronary arteries",
    )
    mock_model = MedicalAnatomyIdentifierModel(
        identification=mock_data, summary="Heart info", data_available=True
    )
    mock_output = ModelOutput(data=mock_model, data_available=True)

    anatomy_identifier.client.generate_text.return_value = mock_output

    # Execute
    result = anatomy_identifier.identify("Heart")

    # Assert
    assert result.data.identification.structure_name == "Heart"
    assert result.data.identification.is_well_known is True
    assert anatomy_identifier.client.generate_text.called


def test_identify_empty_name(anatomy_identifier):
    with pytest.raises(ValueError, match=".+"):
        anatomy_identifier.identify("")
