import io
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch

from article_summary_cli import main


@patch("article_summary_cli.ArticleSummarizer")
def test_cli_text_input(mock_summarizer_class):
    """Test CLI with direct text input."""
    # Setup mock
    mock_summarizer = MagicMock()
    mock_summarizer_class.return_value = mock_summarizer
    mock_summarizer.summarize_article.return_value = "Test Summary"

    with patch("article_summary_cli.Path.mkdir"), patch(
        "builtins.open", new_callable=MagicMock
    ):
        with patch("sys.argv", ["article_summary_cli.py", "-t", "some text"]):
            f = io.StringIO()
            with redirect_stdout(f):
                result = main()
            output = f.getvalue()

    assert result == 0
    assert "Item 1 Summary:" in output
    assert "Test Summary" in output
    mock_summarizer.summarize_article.assert_called_once()


@patch("article_summary_cli.ArticleSummarizer")
def test_cli_file_input(mock_summarizer_class, tmp_path):
    """Test CLI with file input."""
    dummy_file = tmp_path / "test.txt"
    dummy_file.write_text("file content")

    # Setup mock
    mock_summarizer = MagicMock()
    mock_summarizer_class.return_value = mock_summarizer
    mock_summarizer.load_file.return_value = [{"id": "1", "text": "file content"}]
    mock_summarizer.summarize_article.return_value = "File Summary"

    with patch("article_summary_cli.Path.mkdir"), patch(
        "builtins.open", new_callable=MagicMock
    ):
        with patch("sys.argv", ["article_summary_cli.py", "-f", str(dummy_file)]):
            f = io.StringIO()
            with redirect_stdout(f):
                result = main()
            output = f.getvalue()

    assert result == 0
    assert "File Summary" in output
    mock_summarizer.load_file.assert_called_once_with(str(dummy_file))


@patch("article_summary_cli.ArticleSummarizer")
def test_cli_error_handling(mock_summarizer_class):
    """Test CLI error handling."""
    mock_summarizer_class.side_effect = Exception("Summarizer Error")

    with patch("sys.argv", ["article_summary_cli.py", "-t", "text"]):
        with patch("sys.stderr", new=io.StringIO()) as mock_stderr:
            result = main()
            stderr_output = mock_stderr.getvalue()

    assert result == 1
    assert "Error: Summarizer Error" in stderr_output
