import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from article_keywords.cli import main
import io
from contextlib import redirect_stdout


@patch("article_keywords.cli.KeywordExtractor")
def test_cli_text_input(mock_extractor_class):
    """Test CLI with direct text input."""
    # Setup mock
    mock_extractor = MagicMock()
    mock_extractor_class.return_value = mock_extractor
    
    mock_extractor.load_results.return_value = []
    mock_extractor.extract_keywords.return_value = {
        "id": "1",
        "keywords": ["test1", "test2"]
    }
    
    # Mock output directory creation and file saving
    with patch("article_keywords.cli.Path.mkdir"), \
         patch("article_keywords.cli.Path.parent", new=Path("/tmp/fake_parent")):
        
        with patch("sys.argv", ["cli.py", "-t", "some text"]):
            f = io.StringIO()
            with redirect_stdout(f):
                result = main()
            output = f.getvalue()
    
    assert result == 0
    assert "Item 1:" in output
    assert "Keywords (2):" in output
    assert "- test1" in output
    assert "- test2" in output
    
    mock_extractor.extract_keywords.assert_called_once_with("some text", "1")
    mock_extractor.save_results.assert_called_once()


@patch("article_keywords.cli.KeywordExtractor")
def test_cli_file_input(mock_extractor_class, tmp_path):
    """Test CLI with file input."""
    # Create a dummy file
    dummy_file = tmp_path / "test.txt"
    dummy_file.write_text("file content")
    
    # Setup mock
    mock_extractor = MagicMock()
    mock_extractor_class.return_value = mock_extractor
    
    mock_extractor.load_file.return_value = [{"id": "1", "text": "file content"}]
    mock_extractor.load_results.return_value = []
    mock_extractor.extract_keywords.return_value = {
        "id": "1",
        "keywords": ["kw1"]
    }
    
    with patch("article_keywords.cli.Path.mkdir"):
        with patch("sys.argv", ["cli.py", "-f", str(dummy_file)]):
            f = io.StringIO()
            with redirect_stdout(f):
                result = main()
            output = f.getvalue()
            
    assert result == 0
    mock_extractor.load_file.assert_called_once_with(str(dummy_file))
    mock_extractor.extract_keywords.assert_called_once_with("file content", "1")


@patch("article_keywords.cli.KeywordExtractor")
def test_cli_skip_existing(mock_extractor_class):
    """Test CLI skips already processed items."""
    mock_extractor = MagicMock()
    mock_extractor_class.return_value = mock_extractor
    
    mock_extractor.load_results.return_value = [{"id": "1", "keywords": ["old"]}]
    
    with patch("article_keywords.cli.Path.mkdir"):
        with patch("sys.argv", ["cli.py", "-t", "some text"]):
            f = io.StringIO()
            with redirect_stdout(f):
                result = main()
            output = f.getvalue()
            
    assert result == 0
    assert "Item 1: Keywords already extracted, skipping..." in output
    mock_extractor.extract_keywords.assert_not_called()


@patch("article_keywords.cli.KeywordExtractor")
def test_cli_error_handling(mock_extractor_class):
    """Test CLI error handling."""
    mock_extractor_class.side_effect = Exception("Initialization failed")
    
    with patch("sys.argv", ["cli.py", "-t", "text"]):
        f = io.StringIO()
        with redirect_stdout(f):
            # Error is also printed to stderr, but we can check stdout/stderr
            with patch("sys.stderr", new=io.StringIO()) as mock_stderr:
                result = main()
                stderr_output = mock_stderr.getvalue()
                
    assert result == 1
    assert "Error: Initialization failed" in stderr_output
