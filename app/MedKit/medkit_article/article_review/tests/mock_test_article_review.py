import json
from unittest.mock import MagicMock, patch

import pytest
from article_review.article_review import ArticleReviewer


@pytest.fixture
def reviewer():
    """Fixture to provide an ArticleReviewer instance with mocked LiteClient."""
    with patch("article_review.article_review.LiteClient") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        reviewer = ArticleReviewer(model="test-model")
        reviewer.client = mock_instance
        return reviewer


def test_load_file_text(reviewer, tmp_path):
    """Test loading a text file."""
    txt_file = tmp_path / "test.txt"
    content = "Sample article content."
    txt_file.write_text(content)

    text = reviewer.load_file(str(txt_file))
    assert text == content


def test_load_file_json(reviewer, tmp_path):
    """Test loading a JSON file."""
    json_file = tmp_path / "test.json"
    data = {"text": "Nested content", "details": ["More text"]}
    with open(json_file, "w") as f:
        json.dump(data, f)

    text = reviewer.load_file(str(json_file))
    assert "Nested content" in text
    assert "More text" in text


def test_review_article_success(reviewer):
    """Test successful article review."""
    mock_response = MagicMock()
    mock_response.title = "Test Article"
    mock_response.summary = "A good summary."
    mock_response.strengths = ["S1"]
    mock_response.weaknesses = ["W1"]
    mock_response.clinical_implications = "Clinical."
    mock_response.overall_quality = "High"
    reviewer.client.generate_text.return_value = mock_response

    result = reviewer.review_article("Text to review")

    assert result == mock_response
    reviewer.client.generate_text.assert_called_once()


def test_review_article_failure(reviewer):
    """Test failure during article review."""
    reviewer.client.generate_text.side_effect = Exception("API Error")

    result = reviewer.review_article("Text to review")
    assert result is None
