import io
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch

from article_review.article_review_cli import main


@patch("article_review.article_review_cli.ArticleReviewer")
def test_cli_success(mock_reviewer_class, tmp_path):
    """Test CLI success."""
    # Dummy input file
    dummy_file = tmp_path / "article.md"
    dummy_file.write_text("article content")

    # Mocking reviewer
    mock_reviewer = MagicMock()
    mock_reviewer_class.return_value = mock_reviewer
    mock_reviewer.load_file.return_value = "article content"

    mock_review = MagicMock()
    mock_review.title = "Test Article"
    mock_review.summary = "A summary."
    mock_review.strengths = ["S1"]
    mock_review.weaknesses = ["W1"]
    mock_review.clinical_implications = "Clin."
    mock_review.overall_quality = "High"
    mock_review.model_dump.return_value = {"title": "Test"}

    mock_reviewer.review_article.return_value = mock_review

    # Mock Path.mkdir and file opening for saving
    with patch("article_review.article_review_cli.Path.mkdir"), patch(
        "builtins.open", new_callable=MagicMock
    ):
        with patch("sys.argv", ["article_review_cli.py", "-f", str(dummy_file)]):
            f = io.StringIO()
            with redirect_stdout(f):
                result = main()
            output = f.getvalue()

    assert result == 0
    assert "--- Article Review: Test Article ---" in output
    assert "Summary:" in output
    assert "Strengths:" in output
    mock_reviewer.review_article.assert_called_once_with("article content")


@patch("article_review.article_review_cli.ArticleReviewer")
def test_cli_failure(mock_reviewer_class, tmp_path):
    """Test CLI when review fails."""
    dummy_file = tmp_path / "article.md"
    dummy_file.write_text("article content")

    mock_reviewer = MagicMock()
    mock_reviewer_class.return_value = mock_reviewer
    mock_reviewer.review_article.return_value = None

    with patch("sys.argv", ["article_review_cli.py", "-f", str(dummy_file)]):
        f = io.StringIO()
        with redirect_stdout(f):
            result = main()

    assert result == 1
    assert "Review failed." in f.getvalue()


@patch("article_review.article_review_cli.ArticleReviewer")
def test_cli_exception(mock_reviewer_class, tmp_path):
    """Test CLI when an exception occurs."""
    dummy_file = tmp_path / "article.md"
    dummy_file.write_text("article content")

    mock_reviewer_class.side_effect = Exception("Boom")

    with patch("sys.argv", ["article_review_cli.py", "-f", str(dummy_file)]):
        with patch("sys.stderr", new=io.StringIO()) as mock_stderr:
            result = main()
            stderr_output = mock_stderr.getvalue()

    assert result == 1
    assert "Error: Boom" in stderr_output
