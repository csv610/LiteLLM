import unittest
import os
from MathEquationStory.nonagentic.math_equation_story_generator import MathEquationStoryGenerator

class LiveTestMathEquationStory(unittest.TestCase):
    def test_live_generate_text(self):
        print("\nStarting live test for MathEquationStory...")
        model = os.getenv("DEFAULT_LLM_MODEL", "gemini/gemini-2.5-flash")
        generator = MathEquationStoryGenerator(model_name=model)
        
        equation = "E=mc²"
        result = generator.generate_text(equation)
        
        self.assertIsNotNone(result)
        self.assertTrue(len(result.equation_name) > 0)
        self.assertTrue(hasattr(result, "story"))
        self.assertTrue(hasattr(result, "discussion_questions"))
        print("\nLive test completed successfully.")

if __name__ == "__main__":
    unittest.main()
