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
from PeriodicTable.nonagentic.periodic_table_element import PeriodicTableElement
from PeriodicTable.nonagentic.periodic_table_models import ElementInfo

class LiveTestPeriodicTableElement(unittest.TestCase):
    def test_live_nonagentic(self):
        print(f"\nStarting live test for PeriodicTable (nonagentic)...")
        model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:12b-cloud")
        model_config = ModelConfig(model=model, temperature=0.3)
        instance = PeriodicTableElement(model_config)
        
        input_data = 'Gold'
        
        if isinstance(input_data, tuple):
            result = instance.fetch_element_info(*input_data)
        else:
            result = instance.fetch_element_info(input_data)
        
        self.assertIsNotNone(result)
        print(f"\nLive test for PeriodicTable (nonagentic) completed successfully.")

if __name__ == "__main__":
    unittest.main()
