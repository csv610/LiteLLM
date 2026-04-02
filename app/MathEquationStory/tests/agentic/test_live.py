import unittest
import os
import sys
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from MathEquationStory.agentic.math_equation_story_generator import (
    MathEquationStoryGenerator,
)


class LiveTestMathEquationStoryGenerator(unittest.TestCase):
    def test_live_agentic(self):
        print(f"\nStarting live test for MathEquationStory (agentic)...")
        model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:12b-cloud")
        instance = MathEquationStoryGenerator(model_name=model, temperature=0.3)

        result = instance.generate_text("E=mc^2")

        self.assertIsNotNone(result)
        print(f"\nLive test for MathEquationStory (agentic) completed successfully.")


if __name__ == "__main__":
    unittest.main()
