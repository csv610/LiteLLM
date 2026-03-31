import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import MagicMock, patch

import pytest
from lite.config import ModelConfig

from medical.med_media.agentic.med_media import MedicalMediaGenerator


@pytest.fixture
def mock_lite_client():
    with patch("medical.med_media.agentic.med_media.LiteClient") as mock:
        yield mock


@pytest.fixture
def mock_ddg_images():
    with patch("medical.med_media.agentic.med_media.DuckDuckImages") as mock:
        yield mock


@pytest.fixture
def mock_ddg_videos():
    with patch("medical.med_media.agentic.med_media.DuckDuckVideos") as mock:
        yield mock


@pytest.fixture
def generator(mock_lite_client, mock_ddg_images, mock_ddg_videos):
    mock_config = MagicMock(spec=ModelConfig)
    mock_config.model = "test-model"
    return MedicalMediaGenerator(mock_config)


def test_download_images(mock_ddg_images, generator):
    mock_ddg_images_instance = generator.image_searcher
    mock_ddg_images_instance.get_urls.return_value = ["http://example.com/1.jpg"]
    mock_ddg_images_instance.download_image.return_value = "image_1.jpg"

    output_dir = Path("test_outputs")
    downloaded = generator.download_images(
        "test query", num_images=1, output_dir=output_dir
    )

    assert len(downloaded) == 1
    assert downloaded[0] == output_dir / "image_1.jpg"
    mock_ddg_images_instance.get_urls.assert_called_with("test query", "Medium", 1)
    mock_ddg_images_instance.download_image.assert_called_with(
        "http://example.com/1.jpg", str(output_dir), "test query", 0
    )


def test_search_videos(mock_ddg_videos, generator):
    mock_ddg_videos_instance = generator.video_searcher
    mock_ddg_videos_instance.get_urls.return_value = [
        {"url": "http://video.com", "title": "Video 1"}
    ]

    results = generator.search_videos("test query", max_results=1)

    assert len(results) == 1
    assert results[0]["title"] == "Video 1"
    mock_ddg_videos_instance.get_urls.assert_called_with("test query", 1)


def test_generate_caption(mock_lite_client, generator):
    mock_client_instance = generator.client
    mock_client_instance.generate_text.return_value = "Caption result"

    result = generator.generate_caption("test topic")

    assert result == "Caption result"
    mock_client_instance.generate_text.assert_called_once()
    assert generator.last_topic == "test topic"


def test_generate_summary(mock_lite_client, generator):
    mock_client_instance = generator.client
    mock_client_instance.generate_text.return_value = "Summary result"

    result = generator.generate_summary("test topic")

    assert result == "Summary result"
    mock_client_instance.generate_text.assert_called_once()
    assert generator.last_topic == "test topic"


@patch("medical.med_media.agentic.med_media.save_model_response")
def test_save(mock_save_model_response, generator):
    generator.last_topic = "Test Topic"
    result = MagicMock()
    output_dir = Path("test_outputs")

    generator.save(result, output_dir)

    mock_save_model_response.assert_called_with(
        result, output_dir / "test_topic_analysis"
    )
