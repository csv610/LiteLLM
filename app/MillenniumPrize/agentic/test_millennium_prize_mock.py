import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys
import tempfile
import io
from contextlib import redirect_stdout, redirect_stderr

# Mock missing modules before importing the CLI
mock_lite = MagicMock()
sys.modules['lite'] = mock_lite
sys.modules['lite.config'] = MagicMock()
sys.modules['lite.logging_config'] = MagicMock()

# Add current directory to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from millennium_prize_agents import (
    ExplanationGenerationAgent,
    ProblemSelectionAgent,
    TwoAgentWorkflow,
)
from millennium_prize_models import MillenniumProblem, MillenniumProblemsResponse
from millennium_prize_prompts import PromptBuilder
import millennium_prize_problems_cli

class TestMillenniumPrize(unittest.TestCase):

    def setUp(self):
        self.sample_problem_data = {
            "title": "Test Problem",
            "description": "A test description",
            "field": "Mathematics",
            "status": "Unsolved",
            "significance": "High",
            "current_progress": "None"
        }
        self.problem = MillenniumProblem(**self.sample_problem_data)

    def test_millennium_problem_model(self):
        """Test MillenniumProblem model validation."""
        problem = MillenniumProblem(**self.sample_problem_data)
        self.assertEqual(problem.title, "Test Problem")
        self.assertEqual(problem.status, "Unsolved")
        self.assertIsNone(problem.solver)

    def test_millennium_problems_response_model(self):
        """Test MillenniumProblemsResponse model validation."""
        response = MillenniumProblemsResponse(
            total_problems=1,
            problems=[self.problem]
        )
        self.assertEqual(response.total_problems, 1)
        self.assertEqual(len(response.problems), 1)

    def test_prompt_builder_explanation_prompt(self):
        """Test PromptBuilder.create_explanation_prompt."""
        prompt = PromptBuilder.create_explanation_prompt(self.problem)
        self.assertIn("Test Problem", prompt)
        self.assertIn("A test description", prompt)
        self.assertIn("Mathematics", prompt)

    def test_prompt_builder_complete_prompt_data(self):
        """Test PromptBuilder.create_complete_prompt_data."""
        data = PromptBuilder.create_complete_prompt_data(self.problem)
        self.assertIn("prompt", data)
        self.assertIn("model_input", data)
        self.assertEqual(data["model_input"]["user_prompt"], data["prompt"])

    def test_problem_selection_agent_prepares_payload(self):
        """Test ProblemSelectionAgent selection and prompt preparation."""
        agent = ProblemSelectionAgent([self.sample_problem_data])
        payload = agent.prepare_problem_payload(1)
        self.assertEqual(payload["problem_number"], 1)
        self.assertEqual(payload["problem"].title, "Test Problem")
        self.assertIn("Test Problem", payload["prompt"])

    @patch('millennium_prize_agents.LiteClient')
    @patch('millennium_prize_agents.ModelConfig')
    def test_explanation_generation_agent_returns_text(self, mock_model_config, mock_lite_client):
        """Test ExplanationGenerationAgent generates a string explanation."""
        mock_lite_client.return_value.generate_text.return_value = "Agent explanation"
        agent = ExplanationGenerationAgent("ollama/gemma3")
        explanation = agent.generate_explanation("Explain this")
        self.assertEqual(explanation, "Agent explanation")

    def test_explanation_generation_agent_skips_when_model_is_none(self):
        """Test ExplanationGenerationAgent returns an empty string without a model."""
        agent = ExplanationGenerationAgent(None)
        self.assertEqual(agent.generate_explanation("Explain this"), "")

    @patch('millennium_prize_agents.LiteClient')
    @patch('millennium_prize_agents.ModelConfig')
    def test_two_agent_workflow_treats_empty_response_as_completed(self, mock_model_config, mock_lite_client):
        """Test workflow marks an empty model response as completed rather than failed."""
        mock_lite_client.return_value.generate_text.return_value = ""
        workflow = TwoAgentWorkflow([self.sample_problem_data], "ollama/gemma3")
        result = workflow.process_problem(1)
        self.assertEqual(result["explanation"], "")
        self.assertEqual(result["agents"]["explanation_agent"]["status"], "completed")

    @patch('millennium_prize_agents.LiteClient')
    @patch('millennium_prize_agents.ModelConfig')
    def test_two_agent_workflow_marks_generation_exception_as_failed(self, mock_model_config, mock_lite_client):
        """Test workflow marks explanation generation exceptions as failed."""
        mock_lite_client.return_value.generate_text.side_effect = RuntimeError("generation failed")
        workflow = TwoAgentWorkflow([self.sample_problem_data], "ollama/gemma3")
        result = workflow.process_problem(1)
        self.assertEqual(result["explanation"], "")
        self.assertEqual(result["agents"]["explanation_agent"]["status"], "failed")
        self.assertEqual(result["agents"]["explanation_agent"]["model"], "ollama/gemma3")

    def test_two_agent_workflow_skips_explanation_when_requested(self):
        """Test workflow skips explanation generation when instructed."""
        workflow = TwoAgentWorkflow([self.sample_problem_data], "ollama/gemma3")
        result = workflow.process_problem(1, skip_explanation=True)
        self.assertEqual(result["explanation"], "")
        self.assertEqual(result["agents"]["explanation_agent"]["status"], "skipped")
        self.assertIsNone(result["agents"]["explanation_agent"]["model"])

    def test_cli_main_list_all(self):
        """Test CLI main function with list all option (no problem number)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            try:
                with patch.object(sys, 'argv', ['millennium_prize_problems_cli.py']):
                    stdout = io.StringIO()
                    output_file = "millennium_prize_problems.json"
                    with redirect_stdout(stdout):
                        result = millennium_prize_problems_cli.main()

                    self.assertEqual(result, 0)
                    self.assertTrue(os.path.exists(output_file))
                    self.assertIn("Successfully generated output for 7 Millennium Prize Problem(s)", stdout.getvalue())

                    with open(output_file, 'r') as f:
                        data = json.load(f)
                        self.assertEqual(data["title"], "Millennium Prize Problems")
                        self.assertEqual(len(data["problems"]), 7)
            finally:
                os.chdir(original_cwd)

    @patch('millennium_prize_agents.LiteClient')
    @patch('millennium_prize_agents.ModelConfig')
    def test_cli_main_single_problem(self, mock_model_config, mock_lite_client):
        """Test CLI main function with a specific problem number."""
        # Mock LiteClient.generate_text
        mock_instance = mock_lite_client.return_value
        mock_instance.generate_text.return_value = "Test generated explanation"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            try:
                with patch.object(sys, 'argv', ['millennium_prize_problems_cli.py', '-p', '1']):
                    stdout = io.StringIO()
                    output_file = "millennium_problem_1.json"
                    with redirect_stdout(stdout):
                        result = millennium_prize_problems_cli.main()

                    self.assertEqual(result, 0)
                    self.assertTrue(os.path.exists(output_file))
                    self.assertIn("Successfully generated output for: P versus NP", stdout.getvalue())

                    with open(output_file, 'r') as f:
                        data = json.load(f)
                        self.assertEqual(data["problem_number"], 1)
                        self.assertEqual(data["problem"]["title"], "P versus NP")
                        self.assertEqual(data["generated_explanation"], "Test generated explanation")
                        self.assertEqual(data["agents"]["selection_agent"]["status"], "completed")
                        self.assertEqual(data["agents"]["explanation_agent"]["status"], "completed")
            finally:
                os.chdir(original_cwd)

    def test_cli_main_single_problem_without_explanation_agent(self):
        """Test CLI with explanation agent disabled."""
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            try:
                with patch.object(
                    sys,
                    'argv',
                    ['millennium_prize_problems_cli.py', '-p', '1', '--no-explanation']
                ):
                    stdout = io.StringIO()
                    output_file = "millennium_problem_1.json"
                    with redirect_stdout(stdout):
                        result = millennium_prize_problems_cli.main()

                    self.assertEqual(result, 0)
                    self.assertTrue(os.path.exists(output_file))
                    self.assertIn("Successfully generated output for: P versus NP", stdout.getvalue())

                    with open(output_file, 'r') as f:
                        data = json.load(f)
                        self.assertNotIn("generated_explanation", data)
                        self.assertEqual(data["agents"]["selection_agent"]["status"], "completed")
                        self.assertEqual(data["agents"]["explanation_agent"]["status"], "skipped")
            finally:
                os.chdir(original_cwd)

    def test_cli_invalid_problem_number(self):
        """Test CLI with an invalid problem number."""
        with patch.object(sys, 'argv', ['millennium_prize_problems_cli.py', '-p', '10']):
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                result = millennium_prize_problems_cli.main()
            self.assertEqual(result, 1)
            self.assertIn("Error: Problem number must be between 1 and 7", stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
