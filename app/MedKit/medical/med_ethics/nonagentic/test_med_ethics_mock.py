import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.med_ethics.med_ethics import MedEthicalQA
from medical.med_ethics.med_ethics_models import (
    EthicalAnalysisModel,
    EthicalPrincipleModel,
    LegalFrameworkModel,
    ModelOutput,
    StakeholderModel,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.med_ethics.med_ethics.LiteClient") as mock:
        yield mock


def test_med_ethical_qa_init():
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)
    assert generator.model_config == config
    assert generator.client is not None


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)
    mock_output = ModelOutput(
        markdown="Ethics analysis in markdown", data_available=True
    )
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Organ transplantation ethics")
    assert result.markdown == "Ethics analysis in markdown"


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)

    mock_data = EthicalAnalysisModel(
        case_title="Organ Transplant",
        summary="Dilemma",
        facts=["Fact"],
        ethical_issues=["Issue"],
        principles=[
            EthicalPrincipleModel(
                principle="Autonomy",
                application="Self-determination",
                implications=["Choice"],
            )
        ],
        stakeholders=[
            StakeholderModel(name="Patient", interests=["Health"], rights=["Care"])
        ],
        legal_considerations=LegalFrameworkModel(
            regulations=["Law"], professional_guidelines=["Guide"]
        ),
        recommendations=["Action"],
        conclusion="Complex topic",
    )
    mock_output = ModelOutput(data=mock_data, data_available=True)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Organ transplantation", structured=True)
    assert result.data.case_title == "Organ Transplant"
