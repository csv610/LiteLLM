import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import MagicMock, patch

import pytest

from medical.med_media.ddg_images import DuckDuckImages


@pytest.fixture
def ddg_images():
    return DuckDuckImages()


@patch("requests.head")
def test_is_valid_image_url(mock_head, ddg_images):
    mock_response = MagicMock()
    mock_response.headers = {"Content-Type": "image/jpeg"}
    mock_head.return_value = mock_response

    assert ddg_images.is_valid_image_url("http://example.com/image.jpg") is True

    mock_response.headers = {"Content-Type": "text/html"}
    assert ddg_images.is_valid_image_url("http://example.com/not_image") is False


@patch("medical.med_media.ddg_images.DDGS")
@patch("medical.med_media.ddg_images.DuckDuckImages.is_valid_image_url")
def test_get_urls(mock_valid, mock_ddgs, ddg_images):
    mock_ddgs_instance = MagicMock()
    mock_ddgs.return_value.__enter__.return_value = mock_ddgs_instance
    mock_ddgs_instance.images.return_value = [
        {"image": "http://example.com/1.jpg"},
        {"image": "http://example.com/2.jpg"},
    ]
    mock_valid.side_effect = [True, False]

    urls = ddg_images.get_urls("query", "Medium", 1)
    assert len(urls) == 1
    assert urls[0] == "http://example.com/1.jpg"


@patch("requests.get")
@patch("PIL.Image.open")
@patch("os.makedirs")
def test_download_image(mock_makedirs, mock_image_open, mock_get, ddg_images):
    mock_response = MagicMock()
    mock_response.content = b"fake image content"
    mock_get.return_value = mock_response

    mock_img = MagicMock()
    mock_img.format = "JPEG"
    mock_image_open.return_value = mock_img

    filename = ddg_images.download_image(
        "http://example.com/1.jpg", "outputs", "test query", 0
    )
    assert filename == "test_query_1.jpeg"
    mock_img.save.assert_called_once()


@patch("requests.get")
@patch("PIL.Image.open")
def test_fetch_image_size(mock_image_open, mock_get, ddg_images):
    mock_response = MagicMock()
    mock_response.content = b"fake image content"
    mock_get.return_value = mock_response

    mock_img = MagicMock()
    mock_img.size = (800, 600)
    mock_image_open.return_value = mock_img

    size = ddg_images.fetch_image_size("http://example.com/1.jpg")
    assert size == (800, 600)
