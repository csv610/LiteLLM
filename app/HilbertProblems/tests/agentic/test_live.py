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
from HilbertProblems.agentic.hilbert_problems import HilbertProblemsGuide
from HilbertProblems.agentic.hilbert_models import HilbertProblemResponse

class LiveTestHilbertProblemsGuide(unittest.TestCase):
    def test_live_agentic(self):
        print(f"\nStarting live test for HilbertProblems (agentic)...")
        model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:12b-cloud")
        model_config = ModelConfig(model=model, temperature=0.3)
        instance = HilbertProblemsGuide(model_config)
        
        schema = HilbertProblemResponse.model_json_schema()
        input_data = 'Continuum Hypothesis'
        if isinstance(input_data, str):
            input_data += f"\n\nReturn ONLY JSON following this schema:\n{json.dumps(schema, indent=2)}"
        
        result = instance.generate_text(input_data)
        
        self.assertIsNotNone(result)
        print(f"\nLive test for HilbertProblems (agentic) completed successfully.")

if __name__ == "__main__":
    unittest.main()
