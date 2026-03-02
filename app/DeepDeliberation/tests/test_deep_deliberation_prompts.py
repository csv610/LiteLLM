import unittest
from deep_deliberation_prompts import PromptBuilder

class TestPromptBuilder(unittest.TestCase):
    def test_get_initial_prompt(self):
        prompt = PromptBuilder.get_initial_prompt("Quantum Physics", 10)
        self.assertIn("Quantum Physics", prompt)
        self.assertIn("10", prompt)
        self.assertIn("Discovery Questions", prompt)

    def test_get_iteration_prompt(self):
        prompt = PromptBuilder.get_iteration_prompt("Topic", "Question", "Rationale", "History")
        self.assertIn("Topic", prompt)
        self.assertIn("Question", prompt)
        self.assertIn("Rationale", prompt)
        self.assertIn("History", prompt)

    def test_get_summary_prompt(self):
        prompt = PromptBuilder.get_summary_prompt("Topic", "Analysis")
        self.assertIn("Topic", prompt)
        self.assertIn("Analysis", prompt)

    def test_get_discovery_check_prompt(self):
        prompt = PromptBuilder.get_discovery_check_prompt("Topic", "Response")
        self.assertIn("Topic", prompt)
        self.assertIn("Response", prompt)

    def test_get_verification_prompt(self):
        prompt = PromptBuilder.get_verification_prompt("Topic", "Analysis", ["Evidence1"])
        self.assertIn("Topic", prompt)
        self.assertIn("Analysis", prompt)
        self.assertIn("Evidence1", prompt)

    def test_get_synthesis_prompt(self):
        prompt = PromptBuilder.get_synthesis_prompt("Topic", ["Resp1", "Resp2"])
        self.assertIn("Topic", prompt)
        self.assertIn("Resp1", prompt)
        self.assertIn("Resp2", prompt)

if __name__ == "__main__":
    unittest.main()
