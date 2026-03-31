import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from unittest.mock import MagicMock, patch

import pytest
from lite.config import ModelConfig

from medical.med_advise.agentic.primary_health_care import PrimaryHealthCareProvider
from medical.med_advise.agentic.primary_health_care_models import (
    ClinicalResponseModel,
    EducationResponseModel,
    ModelOutput,
    PrimaryCareResponseModel,
    SelfCareResponseModel,
    TriageResponseModel,
)


@pytest.fixture
def mock_lite_client():
    # Patch LiteClient in primary_health_care_agents
    with patch("medical.med_advise.agentic.primary_health_care_agents.LiteClient") as mock:
        yield mock


def test_primary_health_care_provider_init():
    config = ModelConfig(model="test-model")
    provider = PrimaryHealthCareProvider(config)
    assert provider.model_config == config
    assert provider.triage_agent is not None
    assert provider.educator_agent is not None
    assert provider.advisor_agent is not None
    assert provider.clinical_agent is not None


def test_generate_text_multi_agent(mock_lite_client):
    config = ModelConfig(model="test-model")
    provider = PrimaryHealthCareProvider(config)

    # Set up mock responses for each agent
    mock_triage_output = MagicMock()
    mock_triage_output.data = TriageResponseModel(
        understanding_concern="Cough", common_symptoms=["Cough", "Fever"]
    )

    mock_edu_output = MagicMock()
    mock_edu_output.data = EducationResponseModel(general_explanation="A chronic cough")

    mock_advisor_output = MagicMock()
    mock_advisor_output.data = SelfCareResponseModel(self_care_advice="Rest")

    mock_clinical_output = MagicMock()
    mock_clinical_output.data = ClinicalResponseModel(
        when_to_seek_care="Fever", next_steps=["See doctor"]
    )

    # Mock sequential calls to generate_text
    # Since all agents share the same LiteClient (mocked), we define side_effect
    mock_instance = mock_lite_client.return_value
    mock_instance.generate_text.side_effect = [
        mock_triage_output,
        mock_edu_output,
        mock_advisor_output,
        mock_clinical_output,
    ]

    result = provider.generate_text("I have a cough", structured=True)

    assert result.data.understanding_concern == "Cough"
    assert "Cough" in result.data.common_symptoms
    assert result.data.general_explanation == "A chronic cough"
    assert result.data.self_care_advice == "Rest"
    assert result.data.when_to_seek_care == "Fever"
    assert "See doctor" in result.data.next_steps

    # Verify markdown is generated
    assert "# Understanding Your Concern" in result.markdown
    assert "Cough" in result.markdown
