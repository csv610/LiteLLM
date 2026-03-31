import pytest
from unittest.mock import patch, MagicMock
import json

from Paradox.agentic.paradox_element import ParadoxExplainer
from Paradox.agentic.paradox_models import (
    ParadoxResponse,
    AudienceLevel,
    ResearchData,
    LogicData,
    DomainData,
)


@pytest.fixture
def mock_lite_client():
    with patch("Paradox.agentic.paradox_element.LiteClient") as mock:
        yield mock


def test_explain_paradox_agentic(mock_lite_client):
    sample = ParadoxResponse(
        title="Ship of Theseus",
        description="If all parts of a ship are replaced over time, is it still the same ship?",
        level=AudienceLevel.PHD,
        explanation="Detailed philosophical analysis...",
        resolution="Modern identity theory perspective...",
        research_data=ResearchData(
            related_theories=["Identity theory", "Four-dimensionalism"]
        ),
        logic_data=LogicData(
            formal_representation="∀x∀y((P(x) ∧ ∀z(z ⊑ x → z ⊑ y)) → x = y)"
        ),
        domain_data=DomainData(related_paradoxes=["Sorites paradox", "Theseus boat"]),
    )
    instance = mock_lite_client.return_value
    instance.generate_text.return_value = sample

    from lite.lite_client import ModelConfig

    mock_config = ModelConfig(model="test-model", temperature=0.2)
    agent = ParadoxExplainer(mock_config)
    result = agent.explain_paradox("Ship of Theseus")

    assert result.title == "Ship of Theseus"
    assert instance.generate_text.call_count == 2
