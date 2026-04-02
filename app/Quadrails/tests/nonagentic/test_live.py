import unittest
import os
from lite.config import ModelConfig
from .guardrail import GuardrailAnalyzer

class LiveTestQuadrails(unittest.IsolatedAsyncioTestCase):
    async def test_live_analyze_text(self):
        print("\nStarting live test for Quadrails...")
        model = os.getenv("DEFAULT_LLM_MODEL", "gemini/gemini-2.5-flash")
        model_config = ModelConfig(model=model, temperature=0.1)
        analyzer = GuardrailAnalyzer(model_config=model_config, max_length=4000)
        
        text = "This is a simple, safe test message."
        result = await analyzer.analyze_text(text, use_cache=False)
        
        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, "is_safe"))
        print("\nLive test completed successfully.")

if __name__ == "__main__":
    unittest.main()
