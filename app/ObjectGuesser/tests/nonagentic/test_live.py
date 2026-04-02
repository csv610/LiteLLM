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
from ObjectGuesser.nonagentic.object_guesser_game import ObjectGuessingGame

class LiveTestObjectGuessingGame(unittest.TestCase):
    def test_live_nonagentic(self):
        print(f"\nStarting live test for ObjectGuesser (nonagentic)...")
        model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:12b-cloud")
        instance = ObjectGuessingGame(model=model, temperature=0.3)
        
        input_data = 'Apple'
        
        # Test getting a question from the LLM
        instance.add_to_history("user", f"I'm thinking of an object (it's a {input_data}).")
        result = instance.get_llm_question()
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        print(f"\nLive test for ObjectGuesser (nonagentic) completed successfully.")

if __name__ == "__main__":
    unittest.main()
