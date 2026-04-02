import unittest
from unittest.mock import patch, MagicMock
from DeepDeliberation.noagentic.deep_deliberation_cli import arguments_parser, main, run_discovery_mission
from DeepDeliberation.noagentic.deep_deliberation_models import KnowledgeSynthesis

class TestCLI(unittest.TestCase):
    def test_argument_parser(self):
        parser = arguments_parser()
        args = parser.parse_args(["-t", "Quantum Computing", "-n", "5", "-f", "10", "-m", "my-model"])
        self.assertEqual(args.topic, "Quantum Computing")
        self.assertEqual(args.num_rounds, 5)
        self.assertEqual(args.num_faqs, 10)
        self.assertEqual(args.model, "my-model")

    @patch('DeepDeliberation.noagentic.deep_deliberation_cli.DeepDeliberation')
    def test_run_discovery_mission(self, mock_dd):
        mock_instance = mock_dd.return_value
        mock_instance.run.return_value = MagicMock(spec=KnowledgeSynthesis)
        
        result = run_discovery_mission("topic", 3, 5, "model", "output")
        
        mock_dd.assert_called_once()
        mock_instance.run.assert_called_with("topic", 3, 5, output_path="output")

    @patch('DeepDeliberation.noagentic.deep_deliberation_cli.run_discovery_mission')
    @patch('sys.stdout')
    def test_main_success(self, mock_stdout, mock_run):
        mock_run.return_value = KnowledgeSynthesis(
            topic="test topic",
            executive_summary="summary",
            hidden_connections=["c1"],
            research_frontiers=["f1"]
        )
        
        with patch('sys.argv', ['cli.py', '-t', 'test topic']):
            exit_code = main()
            self.assertEqual(exit_code, 0)
            mock_run.assert_called_once()

    @patch('DeepDeliberation.noagentic.deep_deliberation_cli.run_discovery_mission')
    @patch('sys.stderr')
    def test_main_failure(self, mock_stderr, mock_run):
        mock_run.side_effect = Exception("error")
        
        with patch('sys.argv', ['cli.py', '-t', 'test topic']):
            exit_code = main()
            self.assertEqual(exit_code, 1)

if __name__ == "__main__":
    unittest.main()
