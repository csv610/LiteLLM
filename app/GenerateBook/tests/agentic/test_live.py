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
from GenerateBook.agentic.bookchapters_generator import BookChaptersGenerator
from GenerateBook.agentic.bookchapters_models import BookChapters

class LiveTestBookChaptersGenerator(unittest.TestCase):
    def test_live_agentic(self):
        print(f"\nStarting live test for GenerateBook (agentic)...")
        model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:12b-cloud")
        model_config = ModelConfig(model=model, temperature=0.3)
        instance = BookChaptersGenerator(model_config)
        
        schema = BookChapters.model_json_schema()
        input_data = 'Artificial Intelligence'
        if isinstance(input_data, str):
            input_data += f"\n\nReturn ONLY JSON following this schema:\n{json.dumps(schema, indent=2)}"
        
        result = instance.generate_text(input_data)
        
        self.assertIsNotNone(result)
        print(f"\nLive test for GenerateBook (agentic) completed successfully.")

if __name__ == "__main__":
    unittest.main()
