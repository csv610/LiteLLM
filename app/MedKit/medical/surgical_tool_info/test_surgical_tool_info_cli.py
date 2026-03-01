import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pytest
from unittest.mock import patch, MagicMock
from medical.surgical_tool_info.surgical_tool_info_cli import get_user_arguments, main_with_args
import argparse

def test_get_user_arguments():
    test_args = ['scalpel', '-d', 'test_outputs', '-m', 'test-model', '-v', '3', '-s']
    with patch('sys.argv', ['surgical_tool_info_cli.py'] + test_args):
        args = get_user_arguments()
        assert args.tool == 'scalpel'
        assert args.output_dir == 'test_outputs'
        assert args.model == 'test-model'
        assert args.verbosity == 3
        assert args.structured is True

@patch('medical.surgical_tool_info.surgical_tool_info_cli.SurgicalToolInfoGenerator')
@patch('medical.surgical_tool_info.surgical_tool_info_cli.configure_logging')
def test_main_with_args_single_tool(mock_configure_logging, mock_generator_class):
    mock_generator = mock_generator_class.return_value
    mock_result = MagicMock()
    mock_generator.generate_text.return_value = mock_result
    
    args = argparse.Namespace(
        tool='scalpel',
        output_dir='test_outputs',
        model='test-model',
        verbosity=2,
        structured=False
    )
    
    with patch('pathlib.Path.mkdir'):
        result = main_with_args(args)
        
    assert result == 0
    mock_generator.generate_text.assert_called_once_with(tool='scalpel', structured=False)
    mock_generator.save.assert_called_once_with(mock_result, Path('test_outputs'))

@patch('medical.surgical_tool_info.surgical_tool_info_cli.SurgicalToolInfoGenerator')
@patch('medical.surgical_tool_info.surgical_tool_info_cli.configure_logging')
def test_main_with_args_file_input(mock_configure_logging, mock_generator_class, tmp_path):
    mock_generator = mock_generator_class.return_value
    mock_result = MagicMock()
    mock_generator.generate_text.return_value = mock_result
    
    tool_file = tmp_path / "tools.txt"
    tool_file.write_text("""scalpel
forceps""")
    
    args = argparse.Namespace(
        tool=str(tool_file),
        output_dir=str(tmp_path / 'outputs'),
        model='test-model',
        verbosity=2,
        structured=True
    )
    
    result = main_with_args(args)
        
    assert result == 0
    assert mock_generator.generate_text.call_count == 2
    mock_generator.generate_text.assert_any_call(tool='scalpel', structured=True)
    mock_generator.generate_text.assert_any_call(tool='forceps', structured=True)

@patch('medical.surgical_tool_info.surgical_tool_info_cli.SurgicalToolInfoGenerator')
@patch('medical.surgical_tool_info.surgical_tool_info_cli.configure_logging')
def test_main_with_args_error(mock_configure_logging, mock_generator_class):
    mock_generator = mock_generator_class.return_value
    mock_generator.generate_text.side_effect = Exception("Test error")
    
    args = argparse.Namespace(
        tool='scalpel',
        output_dir='test_outputs',
        model='test-model',
        verbosity=2,
        structured=False
    )
    
    with patch('pathlib.Path.mkdir'):
        result = main_with_args(args)
        
    assert result == 1
