import unittest
import os
from lite.config import ModelConfig
from faq_generator import FAQGenerator, FAQInput

class LiveTestFAQGenerator(unittest.TestCase):
    def test_live_generate(self):
        print("\nStarting live test for FAQGenerator...")
        model = os.getenv("DEFAULT_LLM_MODEL", "gemini/gemini-2.5-flash")
        model_config = ModelConfig(model=model, temperature=0.3)
        generator = FAQGenerator(model_config=model_config)
        
        faq_input = FAQInput(
            input_source="Python Programming",
            num_faqs=2,
            difficulty="simple",
            output_dir="."
        )
        
        results = generator.generate_text(faq_input)
        
        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)
        self.assertTrue(hasattr(results[0], "question"))
        self.assertTrue(hasattr(results[0], "answer"))
        print("\nLive test completed successfully.")

if __name__ == "__main__":
    unittest.main()
