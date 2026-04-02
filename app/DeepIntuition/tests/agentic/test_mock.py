import pytest
from unittest.mock import patch, MagicMock
import json
from typing import Optional

from app.DeepIntuition.agentic.deep_intuition import DeepIntuition
from app.DeepIntuition.agentic.deep_intuition_models import DeepIntuitionStory, HistoricalResearch, IntuitionInsight, CounterfactualAnalysis, StruggleNarrative
from lite.config import ModelConfig

@pytest.fixture
def mock_lite_client():
    with patch('app.DeepIntuition.agentic.deep_intuition.LiteClient') as mock:
        yield mock

@pytest.fixture
def sample_story():
    return DeepIntuitionStory(
        topic="Einstein",
        the_human_struggle="Years in the patent office, struggling with classical physics",
        the_aha_moment="Imagining riding a light beam; realizing simultaneity is relative",
        human_triumph_rationale="The triumph of intuition over established mathematical formalisms",
        counterfactual_world="Physics would have languished in the ether theory for decades",
        modern_resonance="Basis for GPS and modern physics",
        key_historical_anchors=["Patent Office", "Bern", "Maxwell's Equations"]
    )

def test_generate_story_agentic(mock_lite_client, sample_story):
    # Setup mock to return the correct models for each step
    historical = HistoricalResearch(key_historical_anchors=["Patent Office"], archive_of_failures_details="Failed to find ether drift")
    intuition = IntuitionInsight(the_aha_moment="Light beam ride", intuitive_analogy="Train and lightning", core_insight_summary="Relativity of simultaneity")
    counterfactual = CounterfactualAnalysis(counterfactual_world="Slower progress", modern_resonance="GPS")
    struggle = StruggleNarrative(the_human_struggle="Math vs Intuition", human_triumph_rationale="Persistence")
    
    with patch('app.DeepIntuition.agentic.deep_intuition.LiteClient') as mock_client_class:
        instance = mock_client_class.return_value
        instance.generate_text.side_effect = [historical, intuition, counterfactual, struggle, sample_story]
        
        agent = DeepIntuition(ModelConfig(model="mock"))
        result = agent.generate_story("Einstein")
        
        assert result.topic == "Einstein"
        assert instance.generate_text.call_count == 5
        assert result.the_aha_moment == "Imagining riding a light beam; realizing simultaneity is relative"
