import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)
from unittest.mock import MagicMock, patch

import pytest
from lite.config import ModelConfig

from ..imaging_finding.imaging_finding_models import (
    ImagingFindingIdentificationModel,
    ImagingFindingIdentifierModel,
    ModelOutput,
)
from ..imaging_finding.imaging_finding_recognizer import ImagingFindingIdentifier


@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)


@pytest.fixture
def identifier(mock_model_config):
    with patch("lite.lite_client.LiteClient"):
        id_obj = ImagingFindingIdentifier(mock_model_config)
        id_obj.client.generate_text = MagicMock()
        return id_obj


def test_identify(identifier):
    mock_data = ImagingFindingIdentificationModel(
        name="Pulmonary nodule",
        description="Common imaging finding",
        finding_name="Pulmonary nodule",
        is_well_known=True,
        common_uses=["Radiology"],
        regulatory_status="N/A",
        industry_significance="Common finding",
        modality="CT",
        typical_location="Lung",
        clinical_relevance="Requires followup",
        differential_diagnosis=["Cancer", "Infection"],
    )
    mock_model = ImagingFindingIdentifierModel(
        identification=mock_data, summary="Finding info", data_available=True
    )
    mock_output = ModelOutput(data=mock_model, data_available=True)
    identifier.client.generate_text.return_value = mock_output

    result = identifier.identify("Pulmonary nodule")
    assert result.data.identification.finding_name == "Pulmonary nodule"
    assert result.data.identification.is_well_known is True
