import pytest
import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch
from article_keywords.keyword_extraction import KeywordExtractor
from article_keywords.models import KeywordList


@pytest.fixture
def extractor():
    """Fixture to provide a KeywordExtractor instance with mocked LiteClient."""
    with patch("article_keywords.keyword_extraction.LiteClient") as mock_client:
        # Mock successful client initialization
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        extractor = KeywordExtractor(model="test-model")
        extractor.client = mock_instance
        return extractor


def test_extract_text_from_object_simple_string(extractor):
    """Test extracting text from a simple string."""
    assert extractor._extract_text_from_object("Hello") == "Hello"


def test_extract_text_from_object_dict(extractor):
    """Test extracting text from a dictionary."""
    data = {"key1": "Value 1", "key2": "Value 2"}
    assert extractor._extract_text_from_object(data) == "Value 1 Value 2"


def test_extract_text_from_object_nested(extractor):
    """Test extracting text from a nested structure."""
    data = {
        "title": "Medical Report",
        "findings": ["Hypertension", "Diabetes"],
        "metadata": {"source": "Hospital A"}
    }
    # Order might vary slightly depending on dict implementation, 
    # but in modern Python it's insertion order.
    # Result: "Medical Report Hypertension Diabetes Hospital A"
    result = extractor._extract_text_from_object(data)
    assert "Medical Report" in result
    assert "Hypertension" in result
    assert "Diabetes" in result
    assert "Hospital A" in result


def test_load_file_json(extractor, tmp_path):
    """Test loading a JSON file."""
    json_file = tmp_path / "test.json"
    data = [{"title": "Item 1"}, {"title": "Item 2"}]
    with open(json_file, "w") as f:
        json.dump(data, f)
    
    items = extractor.load_file(str(json_file))
    assert len(items) == 2
    assert items[0]["id"] == "1"
    assert items[0]["text"] == "Item 1"
    assert items[1]["id"] == "2"
    assert items[1]["text"] == "Item 2"


def test_load_file_markdown(extractor, tmp_path):
    """Test loading a Markdown file."""
    md_file = tmp_path / "test.md"
    content = "# Title\n\nBody content."
    with open(md_file, "w") as f:
        f.write(content)
    
    items = extractor.load_file(str(md_file))
    assert len(items) == 1
    assert items[0]["text"] == content


def test_extract_keywords_success(extractor):
    """Test successful keyword extraction."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.keywords = ["Hypertension", "Diabetes ", "HYPERTENSION"]
    extractor.client.generate_text.return_value = mock_response

    result = extractor.extract_keywords("Patient has hypertension and diabetes.", item_id="42")
    
    assert result["id"] == "42"
    # Deduplicated and sorted: ["diabetes", "hypertension"]
    assert result["keywords"] == ["diabetes", "hypertension"]
    extractor.client.generate_text.assert_called_once()


def test_extract_keywords_failure(extractor):
    """Test failure during keyword extraction."""
    extractor.client.generate_text.side_effect = Exception("API Error")
    
    result = extractor.extract_keywords("Some text")
    assert result is None


def test_save_results(extractor, tmp_path):
    """Test saving results to a file."""
    output_file = tmp_path / "output.json"
    results = [{"id": "1", "keywords": ["a", "b"]}]
    
    extractor.save_results(results, output_file)
    
    assert output_file.exists()
    with open(output_file, "r") as f:
        loaded = json.load(f)
    assert loaded == results


def test_load_results_existing(extractor, tmp_path):
    """Test loading existing results."""
    output_file = tmp_path / "output.json"
    results = [{"id": "1", "keywords": ["a", "b"]}]
    with open(output_file, "w") as f:
        json.dump(results, f)
        
    loaded = extractor.load_results(output_file)
    assert loaded == results


def test_load_results_nonexistent(extractor, tmp_path):
    """Test loading results from a non-existent file."""
    output_file = tmp_path / "nonexistent.json"
    assert extractor.load_results(output_file) == []
