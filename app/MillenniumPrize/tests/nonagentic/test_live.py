import unittest
import os
from lite.config import ModelConfig, ModelInput
from lite import LiteClient
from MillenniumPrize.agentic.millennium_prize_models import MillenniumProblem
from MillenniumPrize.agentic.millennium_prize_prompts import PromptBuilder

class LiveTestMillenniumPrize(unittest.TestCase):
    def test_live_generate_explanation(self):
        print("\nStarting live test for MillenniumPrize...")
        model = os.getenv("DEFAULT_LLM_MODEL", "gemini/gemini-2.5-flash")
        model_config = ModelConfig(model=model, temperature=0.3)
        client = LiteClient(model_config=model_config)
        
        problem = MillenniumProblem(
            title="P versus NP",
            description="Is P equal to NP?",
            field="Computer Science",
            status="Unsolved",
            significance="Fundamental",
            current_progress="Open"
        )
        
        prompt_data = PromptBuilder.create_complete_prompt_data(problem)
        model_input = ModelInput(user_prompt=prompt_data["prompt"])
        
        response = client.generate_text(model_input=model_input)
        
        self.assertIsNotNone(response)
        self.assertTrue(len(str(response)) > 0)
        print("\nLive test completed successfully.")

if __name__ == "__main__":
    unittest.main()
