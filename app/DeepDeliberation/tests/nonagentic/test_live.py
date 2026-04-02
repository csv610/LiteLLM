import unittest
import os
import sys
import json
from pathlib import Path

# Add project root and app directory to sys.path
root = Path(__file__).resolve().parent.parent.parent.parent
app_root = root / "app"
for path in [str(root), str(app_root)]:
    if path not in sys.path:
        sys.path.insert(0, path)

from lite.config import ModelConfig
from DeepDeliberation.nonagentic.deep_deliberation import DeepDeliberation
from DeepDeliberation.nonagentic.deep_deliberation_models import KnowledgeSynthesis

class LiveTestDeepDeliberation(unittest.TestCase):
    def test_live_nonagentic(self):
        print(f"\nStarting live test for DeepDeliberation (nonagentic)...")
        model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:12b-cloud")
        model_config = ModelConfig(model=model, temperature=0.3)
        instance = DeepDeliberation(model_config)
        
        input_data = ('Quantum Computing', 1)
        
        if isinstance(input_data, tuple):
            result = instance.run(*input_data)
        else:
            result = instance.run(input_data)
        
        self.assertIsNotNone(result)
        print(f"\nLive test for DeepDeliberation (nonagentic) completed successfully.")

if __name__ == "__main__":
    unittest.main()
