import pytest
import os
from unittest.mock import patch, MagicMock
from lite.vision.core import _download_from_url, _validate_directory_exists

@patch("urllib.request.urlretrieve")
def test_download_from_url_extensions(mock_retrieve):
    mock_retrieve.return_value = (None, None)
    
    # Test .png
    p1 = _download_from_url("https://ex.com/img.png")
    assert p1.endswith(".png")
    os.remove(p1)
    
    # Test .jpeg
    p2 = _download_from_url("https://ex.com/img.jpeg")
    assert p2.endswith(".jpeg")
    os.remove(p2)
    
    # Test .gif
    p3 = _download_from_url("https://ex.com/img.gif")
    assert p3.endswith(".gif")
    os.remove(p3)

    # Test .jpg (defaults to .jpg in the else block if not .jpeg)
    p4 = _download_from_url("https://ex.com/img.jpg")
    assert p4.endswith(".jpg")
    os.remove(p4)

def test_validate_directory_exists_success(tmp_path):
    d = tmp_path / "exists"
    d.mkdir()
    assert _validate_directory_exists(str(d)) == d
