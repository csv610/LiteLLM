import pytest
import json
from pathlib import Path
from unittest.mock import MagicMock, patch
from article_summary import ArticleSummarizer


@pytest.fixture
def summarizer():
    """Fixture to provide an ArticleSummarizer instance with mocked LiteClient."""
    with patch("article_summary.LiteClient") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        summarizer = ArticleSummarizer(model="test-model")
        summarizer.client = mock_instance
        return summarizer


def test_chunk_text(summarizer):
    """Test text chunking logic."""
    text = "A" * 100
    # chunk_size=30, overlap=10 (0.1 of 100? No, 0.1 of chunk_size? Let's check code)
    # Code says: overlap_size = int(chunk_size * overlap_ratio)
    # So chunk_size=30, overlap=3. step_size = 27.
    chunks = summarizer._chunk_text(text, chunk_size=30, overlap_ratio=0.1)
    
    # 0-30, 27-57, 54-84, 81-111(ends at 100)
    assert len(chunks) == 4
    assert chunks[0] == "A" * 30
    assert chunks[-1] == "A" * 19 # 100 - 81 = 19


def test_summarize_article_single_chunk(summarizer):
    """Test summarization when text fits in a single chunk."""
    mock_response = MagicMock()
    mock_response.summary = "Single chunk summary."
    summarizer.client.generate_text.return_value = mock_response

    result = summarizer.summarize_article("Short text", chunk_size=100)
    
    assert result == "Single chunk summary."
    assert summarizer.client.generate_text.call_count == 1


def test_summarize_article_multi_chunk(summarizer):
    """Test summarization with multiple chunks."""
    # First two calls for chunks, third for final summary
    chunk_resp1 = MagicMock()
    chunk_resp1.summary = "Summary 1"
    chunk_resp2 = MagicMock()
    chunk_resp2.summary = "Summary 2"
    final_resp = MagicMock()
    final_resp.summary = "Final Summary"
    
    summarizer.client.generate_text.side_effect = [chunk_resp1, chunk_resp2, final_resp]

    # chunk_size=5, overlap=0 -> chunks: 0-5, 5-10
    result = summarizer.summarize_article("ABCDEFGHIJ", chunk_size=5, overlap_ratio=0)
    
    assert result == "Final Summary"
    assert summarizer.client.generate_text.call_count == 3


def test_load_file_json(summarizer, tmp_path):
    """Test loading a JSON file."""
    json_file = tmp_path / "test.json"
    data = [{"title": "Art 1"}, {"title": "Art 2"}]
    with open(json_file, "w") as f:
        json.dump(data, f)
    
    items = summarizer.load_file(str(json_file))
    assert len(items) == 2
    assert items[0]["text"] == "Art 1"
    assert items[1]["text"] == "Art 2"
