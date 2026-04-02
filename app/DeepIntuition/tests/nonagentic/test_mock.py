import unittest
from unittest.mock import MagicMock, patch
from .deep_intuition import DeepIntuition
from .deep_intuition_models import DeepIntuitionStory
from lite import ModelConfig

class TestDeepIntuition(unittest.TestCase):
    def setUp(self):
        self.model_config = ModelConfig(model="test-model")
        # Patch LiteClient where it's used in deep_intuition.py
        with patch('DeepIntuition.nonagentic.deep_intuition.LiteClient'):
            self.orchestrator = DeepIntuition(self.model_config)
            self.orchestrator.client = MagicMock()

    def test_generate_story_success(self):
        topic = "Galois Theory"
        
        # Non-agentic version only makes ONE call to the model
        final_story = DeepIntuitionStory(
            topic=topic,
            the_human_struggle="Full struggle...",
            the_aha_moment="Full aha...",
            human_triumph_rationale="Full rationale...",
            counterfactual_world="Full world...",
            modern_resonance="Full resonance...",
            key_historical_anchors=["Galois"]
        )
        
        self.orchestrator.client.generate_text.return_value = final_story

        # Patch MissionArchive where it's used in deep_intuition.py
        with patch('DeepIntuition.nonagentic.deep_intuition.MissionArchive') as mock_archive:
            res = self.orchestrator.generate_story(topic)
            
            self.assertEqual(res.topic, topic)
            self.assertEqual(res.the_aha_moment, "Full aha...")
            self.assertEqual(self.orchestrator.client.generate_text.call_count, 1)

if __name__ == "__main__":
    unittest.main()
