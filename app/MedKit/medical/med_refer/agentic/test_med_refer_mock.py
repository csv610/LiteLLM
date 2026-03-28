import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.med_refer.agentic.med_refer import MedReferral, SymptomAnalysis, SpecialistList


@pytest.fixture
def mock_lite_client():
    with patch("medical.med_refer.agentic.med_refer.LiteClient") as mock:
        yield mock


def test_med_referral_init():
    config = ModelConfig(model="test-model")
    referral = MedReferral(config)
    assert referral.config == config


def test_generate_text_agentic(mock_lite_client):
    config = ModelConfig(model="test-model")
    referral = MedReferral(config)

    # Prepare mock return values for sequential calls
    analysis_mock = SymptomAnalysis(
        symptoms=["heart pain"],
        severity="Urgent",
        affected_body_parts=["Chest"]
    )
    specialists_mock = SpecialistList(
        specialists=["Cardiologist"],
        reasoning="Patient reports chest pain."
    )

    # Set up mock to return values in order
    mock_lite_client.return_value.generate_text.side_effect = [
        analysis_mock,
        specialists_mock
    ]

    result = referral.generate_text("I have heart pain")

    assert "# Medical Referral Analysis" in result
    assert "Cardiologist" in result
    assert "Urgent" in result
    assert "Chest" in result
    assert mock_lite_client.return_value.generate_text.call_count == 2


def test_generate_text_error(mock_lite_client):
    config = ModelConfig(model="test-model")
    referral = MedReferral(config)

    mock_lite_client.return_value.generate_text.side_effect = Exception("API Error")

    result = referral.generate_text("I have heart pain")
    assert "Error: API Error" in result
