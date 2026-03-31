import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.med_ethics.agentic.med_ethics import MedEthicalQA
from medical.med_ethics.agentic.med_ethics_models import (
    EthicalAnalysisModel,
    EthicalPrincipleModel,
    LegalFrameworkModel,
    ModelOutput,
    StakeholderModel,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.med_ethics.agentic.med_ethics.LiteClient") as mock:
        yield mock


def test_med_ethical_qa_init():
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)
    assert generator.model_config == config
    assert generator.client is not None


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)
    mock_output_analyst = ModelOutput(
        markdown="Analyst report", data_available=True
    )
    mock_output_compliance = ModelOutput(
        markdown="Compliance report", data_available=True
    )
    mock_output_synthesis = ModelOutput(
        markdown="Final synthesized report", data_available=True
    )
    mock_output_safety = ModelOutput(
        markdown="Safety audit passed", data_available=True
    )
    
    mock_lite_client.return_value.generate_text.side_effect = [
        mock_output_analyst,
        mock_output_compliance,
        mock_output_synthesis,
        mock_output_safety
    ]

    result = generator.generate_text("Organ transplantation ethics")
    assert result.markdown == "Final synthesized report"
    assert mock_lite_client.return_value.generate_text.call_count == 4


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)

    from medical.med_ethics.agentic.med_ethics_models import (
        AnalystOutput,
        ComplianceOutput,
        SafetyCheckModel,
    )

    mock_analyst_data = AnalystOutput(
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
        ethical_issues=["Issue"],
    )
    
    mock_compliance_data = ComplianceOutput(
        legal_considerations=LegalFrameworkModel(
            regulations=["Law"], professional_guidelines=["Guide"], citations=[]
        )
    )

    mock_final_data = EthicalAnalysisModel(
        case_title="Organ Transplant",
        summary="Dilemma",
        facts=["Fact"],
        ethical_issues=["Issue"],
        principles=mock_analyst_data.principles,
        stakeholders=mock_analyst_data.stakeholders,
        legal_considerations=mock_compliance_data.legal_considerations,
        recommendations=["Action"],
        conclusion="Complex topic",
    )

    mock_safety_data = SafetyCheckModel(
        passed=True,
        critical_omissions=[],
        hallucination_warnings=[],
        recommendations_for_improvement=[]
    )
    
    mock_lite_client.return_value.generate_text.side_effect = [
        ModelOutput(data=mock_analyst_data),
        ModelOutput(data=mock_compliance_data),
        ModelOutput(data=mock_final_data),
        ModelOutput(data=mock_safety_data)
    ]

    result = generator.generate_text("Organ transplantation", structured=True)
    assert result.data.case_title == "Organ Transplant"
    assert mock_lite_client.return_value.generate_text.call_count == 4
