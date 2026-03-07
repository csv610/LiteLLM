import unittest
import os
from lite.config import ModelConfig
from periodic_table_element import PeriodicTableElement

class LiveTestPeriodicTable(unittest.TestCase):
    def test_live_fetch_element(self):
        print("\nStarting live test for PeriodicTable...")
        model = os.getenv("DEFAULT_LLM_MODEL", "gemini/gemini-2.5-flash")
        model_config = ModelConfig(model=model, temperature=0.2)
        fetcher = PeriodicTableElement(model_config=model_config)
        
        element_name = "Hydrogen"
        result = fetcher.fetch_element_info(element_name)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.element_name.lower(), element_name.lower())
        self.assertTrue(hasattr(result, "physical_characteristics"))
        print("\nLive test completed successfully.")

if __name__ == "__main__":
    unittest.main()
