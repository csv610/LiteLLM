import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)
from unittest.mock import MagicMock, patch

import pytest
from lite.config import ModelConfig

from ..med_abbreviation.medical_abbreviation_models import (
    AbbreviationIdentificationModel,
    AbbreviationIdentifierModel,
    ModelOutput,
)
from ..med_abbreviation.medical_abbreviation_recognizer import (
    MedicalAbbreviationIdentifier,
)


@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)


@pytest.fixture
def abbr_identifier(mock_model_config):
    with patch("lite.lite_client.LiteClient"):
        id_obj = MedicalAbbreviationIdentifier(mock_model_config)
        id_obj.client.generate_text = MagicMock()
        return id_obj


def test_identify(abbr_identifier):
    # Setup mock response
    mock_data = AbbreviationIdentificationModel(
        name="COPD",
        description="Respiratory condition abbreviation",
        abbreviation="COPD",
        is_well_known=True,
        common_uses=["Pulmonology"],
        regulatory_status="N/A",
        industry_significance="Common abbreviation",
        full_form="Chronic Obstructive Pulmonary Disease",
        context="Respiratory medicine",
        synonyms=["COLD"],
        related_abbreviations=["FEV1"],
    )
    mock_model = AbbreviationIdentifierModel(
        identification=mock_data, summary="COPD info", data_available=True
    )
    mock_output = ModelOutput(data=mock_model, data_available=True)

    abbr_identifier.client.generate_text.return_value = mock_output

    # Execute
    result = abbr_identifier.identify("COPD")

    # Assert
    assert result.data.identification.abbreviation == "COPD"
    assert result.data.identification.is_well_known is True
    assert abbr_identifier.client.generate_text.called


def test_identify_empty_name(abbr_identifier):
    with pytest.raises(ValueError, match=".+"):
        abbr_identifier.identify("")
