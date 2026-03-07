import pytest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

from hilbert_problems_cli import main, argument_parser

def test_argument_parser():
    parser = argument_parser()
    
    # Test problem number
    args = parser.parse_args(['-p', '1'])
    assert args.problem == 1
    
    # Test model
    args = parser.parse_args(['-m', 'ollama/mistral'])
    assert args.model == 'ollama/mistral'

@patch('hilbert_problems_cli.HilbertProblemsGuide')
def test_main_with_problem(mock_guide_class, capsys):
    # Mocking HilbertProblemsGuide instance
    mock_guide = mock_guide_class.return_value
    mock_problem = MagicMock()
    mock_guide.generate_text.return_value = mock_problem
    
    # Set command line arguments
    with patch.object(sys, 'argv', ['hilbert_problems_cli.py', '-p', '1']):
        main()
        
    mock_guide.generate_text.assert_called_with(1)
    mock_guide_class.display_problem.assert_called_once()

@patch('hilbert_problems_cli.HilbertProblemsGuide')
def test_main_summary(mock_guide_class, capsys):
    mock_guide = mock_guide_class.return_value
    
    with patch.object(sys, 'argv', ['hilbert_problems_cli.py']):
        main()
        
    mock_guide.display_summary.assert_called_once()

@patch('hilbert_problems_cli.HilbertProblemsGuide')
def test_main_invalid_problem(mock_guide_class, capsys):
    with patch.object(sys, 'argv', ['hilbert_problems_cli.py', '-p', '25']):
        main()
    
    captured = capsys.readouterr()
    assert "Invalid problem number: 25" in captured.out
    mock_guide_class.return_value.generate_text.assert_not_called()
