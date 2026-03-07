"""
live_test_deep_deliberation.py - Live integration test for DeepDeliberation engine.

This test performs a real discovery mission using the configured LLM.
"""

import unittest
import os
import shutil
from pathlib import Path
from deep_deliberation import DeepDeliberation
from lite import ModelConfig

class LiveTestDeepDeliberation(unittest.TestCase):
    def setUp(self):
        self.topic = "The impact of hydration on cognitive performance"
        self.model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3")
        self.model_config = ModelConfig(model=self.model, temperature=0.7)
        self.engine = DeepDeliberation(self.model_config)
        
        # Setup temporary output directory
        self.test_output_dir = Path(__file__).parent / "live_test_outputs"
        self.test_output_dir.mkdir(exist_ok=True)

    def tearDown(self):
        # Clean up temporary output directory
        if self.test_output_dir.exists():
            shutil.rmtree(self.test_output_dir)

    def test_live_discovery_mission(self):
        """Perform a single round discovery mission and verify the synthesis."""
        print(f"\nStarting live test with model: {self.model}")
        
        # Run 1 round with 2 initial FAQs to keep it quick
        result = self.engine.run(
            topic=self.topic,
            num_rounds=1,
            num_faqs=2,
            output_path=str(self.test_output_dir / "live_result.json")
        )
        
        # Verify results
        self.assertEqual(result.topic, self.topic)
        self.assertTrue(len(result.executive_summary) > 0)
        self.assertTrue(len(result.hidden_connections) >= 0)
        self.assertTrue(len(result.research_frontiers) >= 0)
        
        # Verify output file exists
        self.assertTrue((self.test_output_dir / "live_result.json").exists())
        
        print("\nLive test completed successfully.")

if __name__ == "__main__":
    unittest.main()
