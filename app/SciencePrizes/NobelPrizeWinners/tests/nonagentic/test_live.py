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
from NobelPrizeWinners.nonagentic.nobel_prize_explorer import NobelPrizeWinnerInfo
from NobelPrizeWinners.nonagentic.nobel_prize_models import PrizeResponse

class LiveTestNobelPrizeWinnerInfo(unittest.TestCase):
    def test_live_nonagentic(self):
        print(f"\nStarting live test for NobelPrizeWinners (nonagentic)...")
        model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:12b-cloud")
        model_config = ModelConfig(model=model, temperature=0.3)
        instance = NobelPrizeWinnerInfo(model_config)
        
        input_data = ('Physics', 2023)
        
        if isinstance(input_data, tuple):
            result = instance.fetch_winners(*input_data)
        else:
            result = instance.fetch_winners(input_data)
        
        self.assertIsNotNone(result)
        print(f"\nLive test for NobelPrizeWinners (nonagentic) completed successfully.")

if __name__ == "__main__":
    unittest.main()
