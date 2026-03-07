import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)
from unittest.mock import MagicMock, patch

import pytest
from lite.config import ModelConfig

from ..medical_coding.medical_coding_models import (
    MedicalCodingIdentificationModel,
    MedicalCodingIdentifierModel,
    ModelOutput,
)
from ..medical_coding.medical_coding_recognizer import MedicalCodingIdentifier


@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)


@pytest.fixture
def identifier(mock_model_config):
    with patch("lite.lite_client.LiteClient"):
        id_obj = MedicalCodingIdentifier(mock_model_config)
        id_obj.client.generate_text = MagicMock()
        return id_obj


def test_identify(identifier):
    mock_data = MedicalCodingIdentificationModel(
        name="ICD-10",
        description="Standard coding system",
        coding_system="ICD-10",
        is_well_known=True,
        common_uses=["Medical coding"],
        regulatory_status="Standard system",
        industry_significance="Global standard",
        version="10",
        organization="WHO",
        standard_reference="ICD-10-CM",
        typical_usage_cases=["Billing", "Diagnosis recording"],
        code_structure="Alpha-numeric",
        maintenance_body="WHO",
    )
    mock_model = MedicalCodingIdentifierModel(
        identification=mock_data, summary="Coding info", data_available=True
    )
    mock_output = ModelOutput(data=mock_model, data_available=True)
    identifier.client.generate_text.return_value = mock_output

    result = identifier.identify("ICD-10")
    assert result.data.identification.coding_system == "ICD-10"
    assert result.data.identification.is_well_known is True
