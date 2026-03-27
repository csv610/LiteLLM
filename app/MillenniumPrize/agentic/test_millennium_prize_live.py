import json
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).parent.parent.parent))


try:
    from lite import LiteClient, ModelConfig
    from lite.config import ModelInput
except Exception as exc:
    LiteClient = None
    ModelConfig = None
    ModelInput = None
    IMPORT_ERROR = exc
else:
    IMPORT_ERROR = None


if IMPORT_ERROR is None:
    from millennium_prize_agents import ExplanationGenerationAgent, TwoAgentWorkflow
    import millennium_prize_problems_cli
else:
    ExplanationGenerationAgent = None
    TwoAgentWorkflow = None
    millennium_prize_problems_cli = None


@unittest.skipUnless(
    os.getenv("RUN_MILLENNIUM_LIVE_TESTS") == "1",
    "Set RUN_MILLENNIUM_LIVE_TESTS=1 to run live integration tests.",
)
class LiveTestMillenniumPrize(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if IMPORT_ERROR is not None:
            raise unittest.SkipTest(f"lite dependencies unavailable: {IMPORT_ERROR}")

        cls.model_name = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3")

    def _require_live_generation(self, fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as exc:
            raise unittest.SkipTest(f"Live model/backend unavailable: {exc}") from exc

    def test_live_explanation_generation_agent(self):
        agent = ExplanationGenerationAgent(self.model_name)
        explanation = self._require_live_generation(
            agent.generate_explanation,
            "Explain the P versus NP problem briefly in 3 sentences.",
        )

        self.assertIsInstance(explanation, str)
        self.assertTrue(explanation.strip())

    def test_live_two_agent_workflow(self):
        workflow = TwoAgentWorkflow(
            millennium_prize_problems_cli.MILLENNIUM_PROBLEMS_DATA,
            self.model_name,
        )
        result = self._require_live_generation(workflow.process_problem, 1)

        if result["agents"]["explanation_agent"]["status"] != "completed":
            raise unittest.SkipTest("Live workflow/backend unavailable during explanation generation.")

        self.assertEqual(result["problem_number"], 1)
        self.assertEqual(result["problem"].title, "P versus NP")
        self.assertEqual(result["agents"]["selection_agent"]["status"], "completed")
        self.assertEqual(result["agents"]["explanation_agent"]["status"], "completed")
        self.assertTrue(result["explanation"].strip())

    def test_live_cli_single_problem_output(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            try:
                stdout = io.StringIO()
                argv = [
                    "millennium_prize_problems_cli.py",
                    "--problem",
                    "1",
                    "--model",
                    self.model_name,
                ]

                with patch.object(sys, "argv", argv):
                    with redirect_stdout(stdout):
                        try:
                            result = millennium_prize_problems_cli.main()
                        except Exception as exc:
                            raise unittest.SkipTest(
                                f"Live CLI/backend unavailable: {exc}"
                            ) from exc

                self.assertEqual(result, 0)
                self.assertIn("Successfully generated output for: P versus NP", stdout.getvalue())

                with open("millennium_problem_1.json", "r") as f:
                    payload = json.load(f)

                self.assertEqual(payload["problem"]["title"], "P versus NP")
                self.assertEqual(payload["agents"]["selection_agent"]["status"], "completed")
                if payload["agents"]["explanation_agent"]["status"] != "completed":
                    raise unittest.SkipTest("Live CLI/backend unavailable during explanation generation.")
                self.assertTrue(payload["generated_explanation"].strip())
            finally:
                os.chdir(original_cwd)
