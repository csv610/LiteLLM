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
from ScholarWork.nonagentic.scholar_work_generator import ScholarWorkGenerator
from ScholarWork.nonagentic.scholar_work_models import ScholarMajorWork

class LiveTestScholarWorkGenerator(unittest.TestCase):
    def test_live_nonagentic(self):
        print(f"\nStarting live test for ScholarWork (nonagentic)...")
        model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:12b-cloud")
        model_config = ModelConfig(model=model, temperature=0.3)
        instance = ScholarWorkGenerator(model_config)
        
        input_data = 'Albert Einstein'
        
        if isinstance(input_data, tuple):
            result = instance.generate_text(*input_data)
        else:
            result = instance.generate_text(input_data)
        
        self.assertIsNotNone(result)
        print(f"\nLive test for ScholarWork (nonagentic) completed successfully.")

if __name__ == "__main__":
    unittest.main()
