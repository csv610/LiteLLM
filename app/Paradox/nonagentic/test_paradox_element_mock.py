import pytest
from unittest.mock import patch
from lite.config import ModelConfig
from .paradox_element import ParadoxExplainer
from .paradox_models import Paradox, ParadoxResponse, AudienceLevel, ParadoxStatus

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.5)

@pytest.fixture
def paradox_explainer(mock_model_config):
    with patch('paradox_element.LiteClient'):
        return ParadoxExplainer(mock_model_config)

@pytest.mark.parametrize("level", list(AudienceLevel))
def test_fetch_paradox_explanation_all_levels(paradox_explainer, level):
    """Verify that the explainer can handle and return data for every audience level."""
    # Setup mock response for the specific level
    mock_paradox = Paradox(
        paradox_name="Test Paradox",
        explanations={
            level: {
                "introduction": f"Intro for {level.value}",
                "status": ParadoxStatus.SOLVED,
                "root_cause": f"Hidden assumptions for {level.value}",
                "key_concepts": ["Concept 1"],
                "historical_context": "History",
                "the_contradiction": "Contradiction",
                "modern_relevance": "Modern",
                "impact_on_thought": "Impact",
                "current_debates": "Debates",
                "resolutions": {
                    "who_solved": "Scientists",
                    "how_it_was_solved": "Methodology",
                    "logical": "Logic",
                    "mathematical": "Math"
                }
            }
        }
    )
    mock_response = ParadoxResponse(paradox=mock_paradox)
    paradox_explainer.client.generate_text.return_value = mock_response
    
    result = paradox_explainer.fetch_paradox_explanation("Test Paradox", [level])
    
    assert result.paradox_name == "Test Paradox"
    assert level in result.explanations
    assert result.explanations[level].status == ParadoxStatus.SOLVED
    assert "Hidden assumptions" in result.explanations[level].root_cause
    paradox_explainer.client.generate_text.assert_called_once()
