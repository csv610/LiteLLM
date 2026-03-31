import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import MagicMock, patch

import pytest

from medical.med_media.agentic.ddg_videos import DuckDuckVideos


@pytest.fixture
def ddg_videos():
    return DuckDuckVideos()


@patch("medical.med_media.agentic.ddg_videos.DDGS")
def test_get_urls(mock_ddgs, ddg_videos):
    mock_ddgs_instance = MagicMock()
    mock_ddgs.return_value.__enter__.return_value = mock_ddgs_instance
    mock_ddgs_instance.videos.return_value = [
        {"url": "http://video1.com", "title": "Video 1", "duration": "10:00"},
        {"url": "http://video2.com", "title": "Video 2", "duration": "05:00"},
    ]

    urls = ddg_videos.get_urls("test query", max_results=2)
    assert len(urls) == 2
    # Should be sorted by duration
    assert urls[0]["title"] == "Video 2"
    assert urls[1]["title"] == "Video 1"


def test_duration_to_seconds(ddg_videos):
    assert ddg_videos._duration_to_seconds("05:00") == 300
    assert ddg_videos._duration_to_seconds("10:00") == 600
    assert ddg_videos._duration_to_seconds("01:10:00") == 4200
    assert ddg_videos._duration_to_seconds("N/A") == float("inf")
    assert ddg_videos._duration_to_seconds("invalid") == float("inf")


def test_sort_by_duration(ddg_videos):
    videos = [
        {"title": "Longer", "duration": "10:00"},
        {"title": "Shorter", "duration": "05:00"},
    ]
    sorted_videos = ddg_videos.sort_by_duration(videos)
    assert sorted_videos[0]["title"] == "Shorter"
    assert sorted_videos[1]["title"] == "Longer"
