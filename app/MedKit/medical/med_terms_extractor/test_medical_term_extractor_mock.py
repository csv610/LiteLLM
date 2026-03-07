import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.med_terms_extractor.medical_term_extractor import MedicalTermExtractor
from medical.med_terms_extractor.medical_term_extractor_models import (
    Disease,
    MedicalTerms,
    Medicine,
    ModelOutput,
    Symptom,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.med_terms_extractor.medical_term_extractor.LiteClient") as mock:
        yield mock


def test_extractor_init():
    config = ModelConfig(model="test-model")
    extractor = MedicalTermExtractor(config)
    assert extractor.model_config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    extractor = MedicalTermExtractor(config)
    mock_output = ModelOutput(markdown="Found: Diabetes", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = extractor.generate_text("Patient has diabetes")
    assert result.markdown == "Found: Diabetes"
    assert extractor.text == "Patient has diabetes"


def test_generate_text_empty():
    config = ModelConfig(model="test-model")
    extractor = MedicalTermExtractor(config)
    with pytest.raises(ValueError, match="Input text cannot be empty"):
        extractor.generate_text("")


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    extractor = MedicalTermExtractor(config)

    mock_data = MedicalTerms(
        diseases=[Disease(name="Diabetes", context="Patient has diabetes")],
        medicines=[Medicine(name="Metformin", context="takes metformin")],
        symptoms=[Symptom(name="Polyuria", context="complains of polyuria")],
    )

    mock_output = ModelOutput(data=mock_data, markdown=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = extractor.generate_text(
        "Patient has diabetes, takes metformin, complains of polyuria", structured=True
    )
    assert result.data.diseases[0].name == "Diabetes"


@patch("medical.med_terms_extractor.medical_term_extractor.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    extractor = MedicalTermExtractor(config)
    mock_output = ModelOutput(markdown="Extracted terms")
    mock_lite_client.return_value.generate_text.return_value = mock_output

    extractor.generate_text("Some medical text")
    extractor.save(mock_output, Path("/tmp"))

    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("medical_terms_extraction")
