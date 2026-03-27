import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys

# Mock missing modules before importing the CLI
mock_lite = MagicMock()
mock_logging_util = MagicMock()
sys.modules['lite'] = mock_lite
sys.modules['lite.config'] = MagicMock()
sys.modules['logging_util'] = mock_logging_util

# Add current directory to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

    @patch('millennium_prize_problems_cli.LiteClient')
    @patch('millennium_prize_problems_cli.ModelConfig')
    @patch('millennium_prize_problems_cli.setup_logging')
    def test_cli_main_list_all(self, mock_setup_logging, mock_model_config, mock_lite_client):
        """Test CLI main function with list all option (no problem number)."""
        # Mock sys.argv
        with patch.object(sys, 'argv', ['millennium_prize_problems_cli.py']):
            # Ensure the output file doesn't exist
            output_file = "millennium_prize_problems.json"
            if os.path.exists(output_file):
                os.remove(output_file)
            
            result = millennium_prize_problems_cli.main()
            
            self.assertEqual(result, 0)
            self.assertTrue(os.path.exists(output_file))
            
            with open(output_file, 'r') as f:
                data = json.load(f)
                self.assertEqual(data["title"], "Millennium Prize Problems")
                self.assertEqual(len(data["problems"]), 7)
            
            # Clean up
            os.remove(output_file)

    @patch('millennium_prize_problems_cli.LiteClient')
    @patch('millennium_prize_problems_cli.ModelConfig')
    @patch('millennium_prize_problems_cli.setup_logging')
    def test_cli_main_single_problem(self, mock_setup_logging, mock_model_config, mock_lite_client):
        """Test CLI main function with a specific problem number."""
        # Mock LiteClient.generate_text
        mock_instance = mock_lite_client.return_value
        mock_instance.generate_text.return_value = "Test generated explanation"
        
        # Mock sys.argv to get problem 1
        with patch.object(sys, 'argv', ['millennium_prize_problems_cli.py', '-p', '1']):
            output_file = "millennium_problem_1.json"
            if os.path.exists(output_file):
                os.remove(output_file)
                
            result = millennium_prize_problems_cli.main()
            
            self.assertEqual(result, 0)
            self.assertTrue(os.path.exists(output_file))
            
            with open(output_file, 'r') as f:
                data = json.load(f)
                self.assertEqual(data["problem_number"], 1)
                self.assertEqual(data["problem"]["title"], "P versus NP")
                self.assertEqual(data["generated_explanation"], "Test generated explanation")
            
            # Clean up
            os.remove(output_file)

    @patch('millennium_prize_problems_cli.setup_logging')
    def test_cli_invalid_problem_number(self, mock_setup_logging):
        """Test CLI with an invalid problem number."""
        with patch.object(sys, 'argv', ['millennium_prize_problems_cli.py', '-p', '10']):
            result = millennium_prize_problems_cli.main()
            self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()
