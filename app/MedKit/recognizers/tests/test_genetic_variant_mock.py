import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)
from unittest.mock import MagicMock, patch

import pytest
from lite.config import ModelConfig

from ..genetic_variant.genetic_variant_models import (
    GeneticVariantIdentificationModel,
    GeneticVariantIdentifierModel,
    ModelOutput,
)
from ..genetic_variant.genetic_variant_recognizer import GeneticVariantIdentifier


@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)


@pytest.fixture
def identifier(mock_model_config):
    with patch("lite.lite_client.LiteClient"):
        id_obj = GeneticVariantIdentifier(mock_model_config)
        id_obj.client.generate_text = MagicMock()
        return id_obj


def test_identify(identifier):
    mock_data = GeneticVariantIdentificationModel(
        name="BRCA1 mutation",
        description="Important genetic variant",
        variant_name="BRCA1",
        is_well_known=True,
        common_uses=["N/A"],
        regulatory_status="N/A",
        industry_significance="Important variant",
        gene="BRCA1",
        variant_type="Mutation",
        chromosomal_location="17q21.31",
        clinical_significance="Pathogenic",
    )
    mock_model = GeneticVariantIdentifierModel(
        identification=mock_data, summary="Variant info", data_available=True
    )
    mock_output = ModelOutput(data=mock_model, data_available=True)
    identifier.client.generate_text.return_value = mock_output

    result = identifier.identify("BRCA1")
    assert result.data.identification.variant_name == "BRCA1"
    assert result.data.identification.is_well_known is True
