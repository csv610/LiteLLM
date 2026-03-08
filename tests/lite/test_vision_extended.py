import os
import pytest
from pathlib import Path
from PIL import Image
from unittest.mock import patch, MagicMock
from lite.vision.collection import collect_images, collect_images_with_info
from lite.vision.core import _download_from_url, _validate_directory_exists

@pytest.fixture
def image_dir(tmp_path):
    d = tmp_path / "images"
    d.mkdir()
    # Create some dummy images
    img1 = Image.new('RGB', (10, 10), color='red')
    img1.save(d / "test1.jpg")
    img2 = Image.new('RGB', (20, 20), color='blue')
    img2.save(d / "test2.png")
    # Create a non-image file
    (d / "not_image.txt").write_text("hello")
    # Create a sub-directory with an image
    sub = d / "sub"
    sub.mkdir()
    img3 = Image.new('RGB', (30, 30), color='green')
    img3.save(sub / "test3.jpg")
    return d

def test_collect_images_basic(image_dir):
    images = collect_images(str(image_dir))
    assert len(images) == 2
    assert any("test1.jpg" in p for p in images)
    assert any("test2.png" in p for p in images)

def test_collect_images_recursive(image_dir):
    images = collect_images(str(image_dir), recursive=True)
    assert len(images) == 3
    assert any("test3.jpg" in p for p in images)

def test_collect_images_formats(image_dir):
    images = collect_images(str(image_dir), formats=["PNG"])
    assert len(images) == 1
    assert "test2.png" in images[0]

def test_collect_images_sort(image_dir):
    # Sort by size (test2.png is likely larger than test1.jpg due to size/format)
    images = collect_images(str(image_dir), sort_by="size")
    assert len(images) == 2
    
    # Sort by date
    images = collect_images(str(image_dir), sort_by="date")
    assert len(images) == 2

def test_collect_images_no_validate(image_dir):
    # Add a file that looks like an image but isn't
    (image_dir / "fake.jpg").write_text("not real image")
    # With validation (default), it should be skipped
    assert len(collect_images(str(image_dir))) == 2
    # Without validation, it should be included
    assert len(collect_images(str(image_dir), validate=False)) == 3

def test_collect_images_with_info(image_dir):
    info_list = collect_images_with_info(str(image_dir))
    assert len(info_list) == 2
    assert "width" in info_list[0]
    assert "height" in info_list[0]

def test_validate_directory_exists_errors(tmp_path):
    with pytest.raises(FileNotFoundError):
        _validate_directory_exists("nonexistent_dir")
    
    f = tmp_path / "file.txt"
    f.write_text("hi")
    with pytest.raises(ValueError, match="Path is not a directory"):
        _validate_directory_exists(str(f))

@patch("urllib.request.urlretrieve")
def test_download_from_url_success(mock_retrieve, tmp_path):
    mock_retrieve.return_value = (None, None)
    url = "https://example.com/image.png"
    path = _download_from_url(url)
    assert os.path.exists(path)
    assert path.endswith(".png")
    os.remove(path)

def test_download_from_url_invalid():
    with pytest.raises(ValueError, match="Invalid URL"):
        _download_from_url("not_a_url")

@patch("urllib.request.urlretrieve")
def test_download_from_url_error(mock_retrieve):
    from urllib.error import URLError
    mock_retrieve.side_effect = URLError("Network down")
    with pytest.raises(ValueError, match="Failed to download"):
        _download_from_url("https://example.com/image.jpg")
