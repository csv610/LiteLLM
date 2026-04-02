import unittest
import os
import sys
import json
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from lite.config import ModelConfig
from DeepIntuition.agentic.deep_intuition import DeepIntuition
from DeepIntuition.agentic.deep_intuition import DeepIntuitionStory

class LiveTestDeepIntuition(unittest.TestCase):
    def test_live_agentic(self):
        print(f"\nStarting live test for DeepIntuition (agentic)...")
        model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:12b-cloud")
        model_config = ModelConfig(model=model, temperature=0.3)
        instance = DeepIntuition(model_config)
        
        input_data = 'The First Moon Landing'
        
        result = instance.generate_story(input_data)
        
        self.assertIsNotNone(result)
        print(f"\nLive test for DeepIntuition (agentic) completed successfully.")

if __name__ == "__main__":
    unittest.main()
