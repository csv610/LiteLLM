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
from UnsolvedProblems.agentic.unsolved_problems_explorer import UnsolvedProblemsExplorer
from UnsolvedProblems.agentic.unsolved_problems_models import UnsolvedProblemResponse


class LiveTestUnsolvedProblemsExplorer(unittest.TestCase):
    def test_live_agentic(self):
        print(f"\nStarting live test for UnsolvedProblems (agentic)...")
        model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:12b-cloud")
        model_config = ModelConfig(model=model, temperature=0.3)
        instance = UnsolvedProblemsExplorer(model_config)

        schema = UnsolvedProblemResponse.model_json_schema()
        input_data = "Dark Matter"
        num_problems = 1
        if isinstance(input_data, str):
            input_data += f"\n\nReturn ONLY JSON following this schema:\n{json.dumps(schema, indent=2)}"

        result = instance.generate_text(input_data, num_problems)

        self.assertIsNotNone(result)
        print(f"\nLive test for UnsolvedProblems (agentic) completed successfully.")


if __name__ == "__main__":
    unittest.main()
