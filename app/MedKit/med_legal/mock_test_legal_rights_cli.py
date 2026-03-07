import pytest
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

from lite.config import ModelConfig

try:
    import med_legal.legal_rights_cli as cli
except ImportError:
    import legal_rights_cli as cli

@patch('legal_rights_cli.print')
def test_list_topics(mock_print, tmp_path):
    # Setup a mock topics list file
    assets_dir = tmp_path / "assets"
    assets_dir.mkdir()
    topics_file = assets_dir / "topics_list.txt"
    topics_file.write_text("Topic 1\nTopic 2\n")
    
    with patch('legal_rights_cli.Path') as mock_path_class:
        mock_file_path = MagicMock()
        mock_file_path.parent = tmp_path
        # When Path(__file__) is called, return mock_file_path
        mock_path_class.return_value = mock_file_path
        
        cli.list_topics()
        
        # Verify print was called, it should print the topics
        mock_print.assert_any_call("  1. Topic 1")
        mock_print.assert_any_call("  2. Topic 2")

def test_get_user_arguments_generate():
    test_args = ['medkit-legal', '-m', 'test-model', 'generate', 'Test Topic', '-c', 'Canada']
    with patch.object(sys, 'argv', test_args):
        args = cli.get_user_arguments()
        assert args.command == 'generate'
        assert args.topic == 'Test Topic'
        assert args.country == 'Canada'
        assert args.model == 'test-model'

def test_get_user_arguments_ls():
    test_args = ['medkit-legal', 'ls']
    with patch.object(sys, 'argv', test_args):
        args = cli.get_user_arguments()
        assert args.command == 'ls'

@patch('legal_rights_cli.list_topics')
def test_main_ls(mock_list_topics):
    test_args = ['medkit-legal', 'ls']
    with patch.object(sys, 'argv', test_args):
        assert cli.main() == 0
        mock_list_topics.assert_called_once()

@patch('legal_rights_cli.list_topics')
def test_main_no_args(mock_list_topics):
    test_args = ['medkit-legal']
    with patch.object(sys, 'argv', test_args):
        assert cli.main() == 0
        mock_list_topics.assert_called_once()

@patch('legal_rights_cli.configure_logging')
@patch('legal_rights_cli.LegalRightsGenerator')
def test_main_generate_success(mock_generator_class, mock_configure_logging, tmp_path):
    test_args = ['medkit-legal', '-m', 'test-model', '-d', str(tmp_path), 'generate', 'Test Topic']
    
    # Mock generator instance
    mock_generator = MagicMock()
    mock_generator_class.return_value = mock_generator
    
    with patch.object(sys, 'argv', test_args):
        assert cli.main() == 0
        
        # Verify logging configured
        mock_configure_logging.assert_called_once()
        
        # Verify generator instantiated and called
        mock_generator_class.assert_called_once()
        mock_generator.generate_text.assert_called_once_with(topic='Test Topic', country='India', structured=False)
        mock_generator.save.assert_called_once()

@patch('legal_rights_cli.configure_logging')
@patch('legal_rights_cli.LegalRightsGenerator')
def test_main_generate_file_input(mock_generator_class, mock_configure_logging, tmp_path):
    # Create a test input file
    input_file = tmp_path / "topics.txt"
    input_file.write_text("Topic A\nTopic B\n")
    
    test_args = ['medkit-legal', '-d', str(tmp_path), 'generate', str(input_file)]
    
    mock_generator = MagicMock()
    mock_generator_class.return_value = mock_generator
    
    with patch.object(sys, 'argv', test_args):
        assert cli.main() == 0
        
        # Should be called twice, once for each topic
        assert mock_generator.generate_text.call_count == 2
        mock_generator.generate_text.assert_any_call(topic='Topic A', country='India', structured=False)
        mock_generator.generate_text.assert_any_call(topic='Topic B', country='India', structured=False)
        assert mock_generator.save.call_count == 2

@patch('legal_rights_cli.configure_logging')
@patch('legal_rights_cli.LegalRightsGenerator')
def test_main_generate_failure(mock_generator_class, mock_configure_logging, tmp_path):
    test_args = ['medkit-legal', '-d', str(tmp_path), 'generate', 'Test Topic']
    
    mock_generator = MagicMock()
    # Make generate_text raise an exception
    mock_generator.generate_text.side_effect = Exception("API Error")
    mock_generator_class.return_value = mock_generator
    
    with patch.object(sys, 'argv', test_args):
        # The main function handles exceptions and returns 1
        assert cli.main() == 1
        mock_generator.save.assert_not_called()
