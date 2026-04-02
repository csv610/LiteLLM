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
from DeepDeliberation.agentic.deep_deliberation import DeepDeliberation
from DeepDeliberation.agentic.deep_deliberation_models import KnowledgeSynthesis

class LiveTestDeepDeliberation(unittest.TestCase):
    def test_live_agentic(self):
        print(f"\nStarting live test for DeepDeliberation (agentic)...")
        model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:12b-cloud")
        model_config = ModelConfig(model=model, temperature=0.3)
        instance = DeepDeliberation(model_config)
        
        topic = 'Quantum Computing'
        num_rounds = 1
        
        result = instance.run(topic, num_rounds)
        
        self.assertIsNotNone(result)
        print(f"\nLive test for DeepDeliberation (agentic) completed successfully.")

if __name__ == "__main__":
    unittest.main()
