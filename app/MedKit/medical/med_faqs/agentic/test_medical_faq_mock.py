import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from lite.config import ModelConfig

# Corrected import for the agentic version
from medical.med_faqs.agentic.medical_faq import MedicalFAQGenerator
from medical.med_faqs.agentic.medical_faq_models import (
    ModelOutput,
    MedicalFAQModel,
    PatientBasicInfoModel,
    ProviderFAQModel,
    SafetyInfoModel,
    ResearchInfoModel,
    ComplianceReviewModel,
    FAQItemModel,
    PatientFAQModel,
)


@pytest.fixture
def mock_lite_client():
    # Mock the LiteClient in the medical_agents module
    with patch("medical.med_faqs.agentic.medical_agents.LiteClient") as mock:
        yield mock


def test_medical_faq_generator_init():
    config = ModelConfig(model="test-model")
    generator = MedicalFAQGenerator(config)
    assert generator.model_config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalFAQGenerator(config)

    # We need to provide a mock response for each of the 5 agents (including Compliance)
    mock_instance = mock_lite_client.return_value
    mock_instance.generate_text.side_effect = [
        ModelOutput(markdown="Patient info"),
        ModelOutput(markdown="Clinical info"),
        ModelOutput(markdown="Safety info"),
        ModelOutput(markdown="Research info"),
        ModelOutput(markdown="Compliance: All clear."),
    ]

    result = generator.generate_text("What is diabetes?", structured=False)
    assert "Patient info" in result.markdown
    assert "Clinical info" in result.markdown
    assert "Safety info" in result.markdown
    assert "Research info" in result.markdown
    assert "Compliance: All clear." in result.markdown


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalFAQGenerator(config)

    # We need to provide structured mock data for each agent
    mock_instance = mock_lite_client.return_value

    # 1. PatientAgent
    patient_info = PatientBasicInfoModel(
        introduction="Intro",
        faqs=[FAQItemModel(question="Q1", answer="A1")]
    )
    # 2. ClinicalAgent
    clinical_info = ProviderFAQModel(
        topic_name="Diabetes",
        clinical_overview="Overview",
        clinical_faqs=[],
        evidence_based_practices=[],
        quality_metrics=[],
        referral_criteria=[]
    )
    # 3. SafetyAgent
    safety_info = SafetyInfoModel(
        when_to_seek_care=[],
        misconceptions=[]
    )
    # 4. ResearchAgent
    research_info = ResearchInfoModel(
        see_also=[]
    )
    # 5. ComplianceAgent
    compliance_info = ComplianceReviewModel(
        is_compliant=True,
        issues_found=[],
        required_disclaimers=["Mandatory disclaimer"],
        suggested_edits=None
    )

    mock_instance.generate_text.side_effect = [
        ModelOutput(data=patient_info),
        ModelOutput(data=clinical_info),
        ModelOutput(data=safety_info),
        ModelOutput(data=research_info),
        ModelOutput(data=compliance_info),
    ]

    result = generator.generate_text("What is diabetes?", structured=True)
    assert result.data.topic_name == "What is diabetes?"
    assert result.data.patient_faq.introduction == "Intro"
    assert result.data.compliance_review.is_compliant is True
    assert "Mandatory disclaimer" in result.data.compliance_review.required_disclaimers
