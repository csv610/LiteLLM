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
from ScholarWork.agentic.scholar_work_generator import ScholarWorkGenerator
from ScholarWork.agentic.scholar_work_models import ScholarMajorWork


class LiveTestScholarWorkGenerator(unittest.TestCase):
    def test_live_agentic(self):
        print(f"\nStarting live test for ScholarWork (agentic)...")
        model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:4b-cloud")
        instance = ScholarWorkGenerator(model_name=model, temperature=0.3)

        input_data = "Albert Einstein"

        result = instance.generate_text(input_data)
        print(f"Raw result type: {type(result)}")
        print(f"Raw result: {result}")

        self.assertIsNotNone(result)
        print(f"\nLive test for ScholarWork (agentic) completed successfully.")


if __name__ == "__main__":
    unittest.main()
