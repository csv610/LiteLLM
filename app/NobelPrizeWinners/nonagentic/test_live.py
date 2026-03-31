import unittest
import os
from .nobel_prize_info import fetch_nobel_winners

class LiveTestNobelPrizeWinners(unittest.TestCase):
    def test_live_fetch_winners(self):
        print("\nStarting live test for NobelPrizeWinners...")
        model = os.getenv("DEFAULT_LLM_MODEL", "gemini/gemini-2.5-flash")
        
        category = "Physics"
        year = "2023"
        winners = fetch_nobel_winners(category, year, model=model)
        
        self.assertIsNotNone(winners)
        self.assertGreaterEqual(len(winners), 1)
        self.assertTrue(hasattr(winners[0], "name"))
        self.assertTrue(hasattr(winners[0], "year"))
        print("\nLive test completed successfully.")

if __name__ == "__main__":
    unittest.main()
