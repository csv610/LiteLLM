import unittest
import os
import sys
import json
from pathlib import Path

# Add app directory to sys.path
root = Path(__file__).parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from lite.config import ModelConfig
from Paradox.agentic.paradox_element import ParadoxExplainer
from Paradox.agentic.paradox_models import Paradox, AudienceLevel

class LiveTestParadoxExplainer(unittest.TestCase):
    def test_live_agentic(self):
        print(f"\nStarting live test for Paradox (agentic)...")
        model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:12b-cloud")
        model_config = ModelConfig(model=model, temperature=0.3)
        instance = ParadoxExplainer(model_config)
        
        # Just pass the name, the agentic system handles the rest
        paradox_name = 'Grandfather Paradox'
        
        # Only fetch for one level to speed up the test
        result = instance.fetch_paradox_explanation(paradox_name, audience_levels=[AudienceLevel.UNDERGRAD])
        
        self.assertIsNotNone(result)
        self.assertEqual(result.paradox_name, paradox_name)
        self.assertIn(AudienceLevel.UNDERGRAD, result.explanations)
        print(f"\nLive test for Paradox (agentic) completed successfully.")

if __name__ == "__main__":
    unittest.main()
