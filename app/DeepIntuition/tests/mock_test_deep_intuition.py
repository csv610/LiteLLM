import unittest
from unittest.mock import MagicMock, patch
from deep_intuition import DeepIntuition
from deep_intuition_models import DeepIntuitionStory
from lite import ModelConfig

class TestDeepIntuition(unittest.TestCase):
    def setUp(self):
        self.model_config = ModelConfig(model="test-model")
        with patch('deep_intuition.LiteClient'):
            self.orchestrator = DeepIntuition(self.model_config)
            self.orchestrator.client = MagicMock()

    def test_generate_story_success(self):
        topic = "Galois Theory"
        
        expected_story = DeepIntuitionStory(
            topic=topic,
            the_human_struggle="Years of exploration...",
            the_aha_moment="The concept of groups clicked.",
            human_triumph_rationale="It was persistence, not magic.",
            counterfactual_world="Math would be stalled.",
            modern_resonance="Used in cryptography.",
            key_historical_anchors=["Evariste Galois"]
        )
        
        self.orchestrator.client.generate_text.return_value = expected_story

        with patch('deep_intuition.MissionArchive') as mock_archive:
            res = self.orchestrator.generate_story(topic)
            
            self.assertEqual(res.topic, topic)
            self.assertEqual(res.the_aha_moment, "The concept of groups clicked.")
            self.orchestrator.client.generate_text.assert_called()

if __name__ == "__main__":
    unittest.main()
