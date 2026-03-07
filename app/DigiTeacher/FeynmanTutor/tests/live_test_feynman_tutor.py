import unittest
import os
import sys
from pathlib import Path

# Need to ensure correct imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from feynman_tutor import FeynmanTutorQuestionGenerator, ModelConfig as FeynmanConfig

class LiveTestFeynmanTutor(unittest.TestCase):
    def test_live_start_tutoring(self):
        print("\nStarting live test for FeynmanTutor...")
        # Note: the local ModelConfig might not support changing the model easily 
        # without environment variable. Let's assume it picks up LiteClient defaults.
        os.environ["DEFAULT_LLM_MODEL"] = "gemini/gemini-2.5-flash"
        
        config = FeynmanConfig(topic="Gravity", level="beginner")
        tutor = FeynmanTutorQuestionGenerator(config)
        
        result = tutor.start_tutoring()
        
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, str))
        self.assertTrue(len(result) > 0)
        print("\nLive test completed successfully.")

if __name__ == "__main__":
    unittest.main()
