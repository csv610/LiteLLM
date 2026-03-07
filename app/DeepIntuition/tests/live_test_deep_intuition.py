import unittest
import os
from lite.config import ModelConfig
from deep_intuition import DeepIntuition

class LiveTestDeepIntuition(unittest.TestCase):
    def test_live_generate_story(self):
        print("\nStarting live test for DeepIntuition...")
        model = os.getenv("DEFAULT_LLM_MODEL", "gemini/gemini-2.5-flash")
        model_config = ModelConfig(model=model, temperature=0.3)
        orchestrator = DeepIntuition(model_config=model_config)
        
        topic = "Galois Theory"
        result = orchestrator.generate_story(topic)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.topic, topic)
        self.assertTrue(hasattr(result, "the_aha_moment"))
        self.assertTrue(hasattr(result, "modern_resonance"))
        print("\nLive test completed successfully.")

if __name__ == "__main__":
    unittest.main()
