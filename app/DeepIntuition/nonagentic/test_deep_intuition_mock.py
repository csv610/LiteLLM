import unittest
from unittest.mock import MagicMock, patch
from DeepIntuition.agentic.deep_intuition import DeepIntuition
from DeepIntuition.agentic.deep_intuition_models import (
    DeepIntuitionStory, 
    HistoricalResearch, 
    IntuitionInsight, 
    CounterfactualAnalysis, 
    StruggleNarrative
)
from lite import ModelConfig

class TestDeepIntuition(unittest.TestCase):
    def setUp(self):
        self.model_config = ModelConfig(model="test-model")
        with patch('DeepIntuition.agentic.deep_intuition.LiteClient'):
            self.orchestrator = DeepIntuition(self.model_config)
            self.orchestrator.client = MagicMock()

    def test_generate_story_success(self):
        topic = "Galois Theory"
        
        # Sequenced responses for the 5 agents
        historical = HistoricalResearch(
            key_historical_anchors=["Evariste Galois"],
            archive_of_failures_details="Failures notes..."
        )
        intuition = IntuitionInsight(
            the_aha_moment="Analogy...",
            intuitive_analogy="Analogy...",
            core_insight_summary="Summary..."
        )
        counterfactual = CounterfactualAnalysis(
            counterfactual_world="World without...",
            modern_resonance="Resonance..."
        )
        struggle = StruggleNarrative(
            the_human_struggle="Struggle...",
            human_triumph_rationale="Rationale..."
        )
        final_story = DeepIntuitionStory(
            topic=topic,
            the_human_struggle="Full struggle...",
            the_aha_moment="Full aha...",
            human_triumph_rationale="Full rationale...",
            counterfactual_world="Full world...",
            modern_resonance="Full resonance...",
            key_historical_anchors=["Galois"]
        )
        
        self.orchestrator.client.generate_text.side_effect = [
            historical, intuition, counterfactual, struggle, final_story
        ]

        with patch('DeepIntuition.agentic.deep_intuition.MissionArchive') as mock_archive:
            res = self.orchestrator.generate_story(topic)
            
            self.assertEqual(res.topic, topic)
            self.assertEqual(res.the_aha_moment, "Full aha...")
            self.assertEqual(self.orchestrator.client.generate_text.call_count, 5)

if __name__ == "__main__":
    unittest.main()
