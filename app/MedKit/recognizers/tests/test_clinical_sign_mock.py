from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from ..clinical_sign.clinical_sign_models import (
    ClinicalSignIdentificationModel,
    ClinicalSignIdentifierModel,
    ModelOutput,
)

# No need for sys.path hacks if we use relative imports and run with pytest from root
from ..clinical_sign.clinical_sign_recognizer import ClinicalSignIdentifier


@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)


@pytest.fixture
def identifier(mock_model_config):
    with patch("lite.lite_client.LiteClient") as mock:
        yield ClinicalSignIdentifier(mock_model_config)


def test_identify(identifier):
    mock_data = ClinicalSignIdentifierModel(
        identification=ClinicalSignIdentificationModel(
            name="Babinski sign",
            description="Important neurological sign",
            sign_name="Babinski",
            is_well_known=True,
            common_uses=["Neurological exam"],
            regulatory_status="Standard",
            industry_significance="Important",
            clinical_relevance="Indicates upper motor neuron lesion",
            common_manifestations=["Upward toe movement"],
            associated_conditions=["Stroke", "ALS"],
        ),
        summary="Important neurological sign.",
        data_available=True,
    )
    mock_output = ModelOutput(data=mock_data, data_available=True)
    identifier.client.generate_text.return_value = mock_output

    result = identifier.identify("Babinski")
    assert result.data.identification.sign_name == "Babinski"
    assert result.data.identification.is_well_known is True


def test_identify_empty():
    config = ModelConfig(model="test")
    with patch("lite.lite_client.LiteClient"):
        identifier = ClinicalSignIdentifier(config)
        with pytest.raises(ValueError, match=".+"):
            identifier.identify("")
