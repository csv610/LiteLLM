import unittest
import os
from hilbert_problems import HilbertProblemsGuide

class LiveTestHilbertProblems(unittest.TestCase):
    def test_live_generate_text(self):
        print("\nStarting live test for HilbertProblems...")
        # Note: HilbertProblemsGuide constructor might not take model_config directly,
        # but we can set the environment variable.
        os.environ["DEFAULT_LLM_MODEL"] = "gemini/gemini-2.5-flash"
        guide = HilbertProblemsGuide()
        
        problem_number = 1
        result = guide.generate_text(problem_number)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.number, problem_number)
        self.assertTrue(hasattr(result, "title"))
        self.assertTrue(hasattr(result, "status"))
        print("\nLive test completed successfully.")

if __name__ == "__main__":
    unittest.main()
