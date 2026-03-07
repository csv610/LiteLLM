import unittest
import os
from lite.config import ModelConfig
from math_theory_element import MathTheoryExplainer
from math_theory_models import AudienceLevel

class LiveTestMathTheory(unittest.TestCase):
    def test_live_fetch_theory(self):
        print("\nStarting live test for MathTheories...")
        model = os.getenv("DEFAULT_LLM_MODEL", "gemini/gemini-2.5-flash")
        model_config = ModelConfig(model=model, temperature=0.2)
        explainer = MathTheoryExplainer(model_config=model_config)
        
        theory_name = "Group theory"
        result = explainer.fetch_theory_explanation(theory_name, audience_levels=[AudienceLevel.UNDERGRAD])
        
        self.assertIsNotNone(result)
        self.assertEqual(result.theory_name, theory_name)
        self.assertTrue(AudienceLevel.UNDERGRAD in result.explanations)
        print("\nLive test completed successfully.")

if __name__ == "__main__":
    unittest.main()
