import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import json

# Add app directory to sys.path
root = Path(__file__).parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from Paradox.agentic.paradox_element import ParadoxExplainer
from Paradox.agentic.paradox_models import (
    Paradox,
    AudienceLevel,
    ParadoxStatus,
    ResearchData,
    LogicData,
    DomainData,
    ParadoxExplanation,
    ParadoxResolution,
)


@pytest.fixture
def mock_lite_client():
    with patch("Paradox.agentic.paradox_element.LiteClient") as mock:
        yield mock


def test_fetch_paradox_explanation_mock(mock_lite_client):
    # Mock data for agents
    mock_research = ResearchData(
        historical_context="Ancient Greek philosophy...",
        status=ParadoxStatus.DEBATED,
        who_solved="Heraclitus, Plutarch, etc."
    )
    
    mock_logic = LogicData(
        root_cause="Identity over time assumptions",
        the_contradiction="A ship replaced piece by piece...",
        impact_on_thought="Foundational for mereology"
    )
    
    mock_domain = DomainData(
        key_concepts=["Mereological essentialism", "Spatio-temporal continuity"],
        modern_relevance="Relevant to AI identity and teleportation",
        how_it_was_solved="Four-dimensionalism or perdurantism",
        logical_resolution="Identity is not just about parts",
        mathematical_resolution="Set theoretic approach to identity"
    )
    
    mock_final = ParadoxExplanation(
        introduction="The Ship of Theseus is a thought experiment...",
        status=ParadoxStatus.DEBATED,
        root_cause="Assumptions about identity",
        key_concepts=["Identity", "Persistence"],
        historical_context="Plutarch's writings...",
        the_contradiction="Is it the same ship?",
        modern_relevance="AI and identity",
        impact_on_thought="Mereology evolution",
        current_debates="Ongoing discussion in metaphysics",
        resolutions=ParadoxResolution(
            who_solved="Various philosophers",
            how_it_was_solved="Different theories of identity",
            logical="Philosophical analysis",
            mathematical="N/A"
        )
    )

    instance = mock_lite_client.return_value
    # Side effect to return different models for different calls
    instance.generate_text.side_effect = [
        mock_research,
        mock_logic,
        mock_domain,
        mock_final
    ]

    from lite import ModelConfig

    mock_config = ModelConfig(model="test-model", temperature=0.2)
    agent = ParadoxExplainer(mock_config)
    result = agent.fetch_paradox_explanation("Ship of Theseus", audience_levels=[AudienceLevel.PHD])

    assert result.paradox_name == "Ship of Theseus"
    assert AudienceLevel.PHD in result.explanations
    assert result.explanations[AudienceLevel.PHD].introduction == "The Ship of Theseus is a thought experiment..."
    assert instance.generate_text.call_count == 4
