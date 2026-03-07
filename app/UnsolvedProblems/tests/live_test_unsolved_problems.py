import unittest
import os
from lite.config import ModelConfig
from unsolved_problems_explorer import UnsolvedProblemsExplorer

class LiveTestUnsolvedProblems(unittest.TestCase):
    def test_live_fetch_unsolved(self):
        print("\nStarting live test for UnsolvedProblems...")
        model = os.getenv("DEFAULT_LLM_MODEL", "gemini/gemini-2.5-flash")
        model_config = ModelConfig(model=model, temperature=0.2)
        explorer = UnsolvedProblemsExplorer(model_config=model_config)
        
        topic = "Mathematics"
        num_problems = 1
        results = explorer.generate_text(topic, num_problems)
        
        self.assertIsNotNone(results)
        self.assertGreaterEqual(len(results), 1)
        self.assertTrue(hasattr(results[0], "title"))
        self.assertTrue(hasattr(results[0], "description"))
        print("\nLive test completed successfully.")

if __name__ == "__main__":
    unittest.main()
