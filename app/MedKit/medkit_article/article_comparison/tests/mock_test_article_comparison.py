import pytest
from unittest.mock import patch
import sys
import os

from article_comparison.article_comparison import ArticleComparator
from article_comparison.article_comparison_models import ComparisonResult, ArticleEvaluation


@pytest.fixture
def mock_lite_client():
    with patch("article_comparison.article_comparison.LiteClient") as mock:
        yield mock


@pytest.fixture
def comparator(mock_lite_client):
    return ArticleComparator(model="dummy-model")


def test_load_file_md(tmp_path, comparator):
    # Create a dummy md file
    p = tmp_path / "test.md"
    p.write_text("Hello World", encoding="utf-8")

    content = comparator.load_file(str(p))
    assert content == "Hello World"


def test_load_file_json(tmp_path, comparator):
    # Create a dummy json file
    p = tmp_path / "test.json"
    p.write_text(
        '{"title": "My Article", "content": "Article Content"}', encoding="utf-8"
    )

    content = comparator.load_file(str(p))
    # _extract_text_from_object will join "My Article" and "Article Content" with " "
    assert "My Article" in content
    assert "Article Content" in content


def test_compare_articles(comparator, mock_lite_client):
    # Setup mock response
    mock_response = ComparisonResult(
        article1_evaluation=ArticleEvaluation(
            strengths=["S1"], weaknesses=["W1"], overall_quality="Q1"
        ),
        article2_evaluation=ArticleEvaluation(
            strengths=["S2"], weaknesses=["W2"], overall_quality="Q2"
        ),
        winner="Article 1",
        comparison_summary="Summary",
    )

    # Mock generate_text to return our ComparisonResult
    comparator.client.generate_text.return_value = mock_response

    result = comparator.compare_articles("Text 1", "Text 2")

    assert result == mock_response
    comparator.client.generate_text.assert_called_once()

    # Verify prompt was built correctly
    args, kwargs = comparator.client.generate_text.call_args
    model_input = kwargs.get("model_input") or args[0]
    assert "Text 1" in model_input.user_prompt
    assert "Text 2" in model_input.user_prompt
    assert model_input.response_format == ComparisonResult


def test_extract_text_from_object(comparator):
    nested_obj = {
        "a": "text a",
        "b": ["item 1", {"c": "text c"}],
        "d": 123,  # should be filtered out by filter(None, ...) if it's not a string
    }
    # Our implementation:
    # _extract_text_from_object(obj) -> str:
    # texts = []
    # if isinstance(obj, dict): ... texts.append(self._extract_text_from_object(value))
    # elif isinstance(obj, list): ... texts.append(self._extract_text_from_object(item))
    # elif isinstance(obj, str): texts.append(obj)
    # return " ".join(filter(None, texts))

    # Actually, if it's 123, it won't be appended to texts.
    # So "text a", "item 1", "text c"
    result = comparator._extract_text_from_object(nested_obj)
    assert "text a" in result
    assert "item 1" in result
    assert "text c" in result
