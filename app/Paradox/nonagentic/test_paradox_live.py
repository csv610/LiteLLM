import unittest
import os
from lite.config import ModelConfig
from .paradox_element import ParadoxExplainer
from .paradox_models import AudienceLevel

class LiveTestParadox(unittest.TestCase):
    def test_live_fetch_paradox(self):
        print("\nStarting live test for Paradox...")
        model = os.getenv("DEFAULT_LLM_MODEL", "gemini/gemini-2.5-flash")
        model_config = ModelConfig(model=model, temperature=0.2)
        explainer = ParadoxExplainer(model_config=model_config)
        
        paradox_name = "Zeno's paradox"
        result = explainer.fetch_paradox_explanation(paradox_name, audience_levels=[AudienceLevel.UNDERGRAD])
        
        self.assertIsNotNone(result)
        self.assertEqual(result.paradox_name, paradox_name)
        self.assertTrue(AudienceLevel.UNDERGRAD in result.explanations)
        print("\nLive test completed successfully.")

if __name__ == "__main__":
    unittest.main()
