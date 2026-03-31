import pytest
from unittest.mock import patch, MagicMock
import json

from Paradox.agentic.paradox_agents import ParadoxAgent
from Paradox.agentic.paradox_models import ParadoxResponse

@pytest.fixture
def mock_lite_client():
    with patch('Paradox.agentic.paradox_agents.LiteClient') as mock:
        yield mock

def test_explain_paradox_agentic(mock_lite_client):
    sample = ParadoxResponse(
        title="Ship of Theseus",
        description="A paradox about identity.",
        explanation="Does an object remain the same if all its parts are replaced?",
        counterarguments=["Identity is structural", "Identity is material"],
        resolution="It's a matter of definition."
    )
    instance = mock_lite_client.return_value
    # Researcher + Reviewer
    instance.generate_text.side_effect = [sample, sample]
    
    agent = ParadoxAgent()
    result = agent.explain_paradox("Ship of Theseus")
    
    assert result.title == "Ship of Theseus"
    assert instance.generate_text.call_count == 2
