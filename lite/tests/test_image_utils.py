import pytest
from PIL import Image
from lite.image_utils import _is_url, _convert_to_rgb

def test_is_url():
    assert _is_url("http://example.com/image.jpg") is True
    assert _is_url("https://example.com/image.jpg") is True
    assert _is_url("/path/to/local/file.jpg") is False
    assert _is_url("ftp://example.com/image.jpg") is False
    assert _is_url("") is False

def test_convert_to_rgb_from_rgba():
    # Create RGBA image
    rgba_img = Image.new("RGBA", (10, 10), (255, 0, 0, 255))
    rgb_img = _convert_to_rgb(rgba_img)
    assert rgb_img.mode == "RGB"
    # Red should remain red
    assert rgb_img.getpixel((0, 0)) == (255, 0, 0)

def test_convert_to_rgb_already_rgb():
    rgb_img = Image.new("RGB", (10, 10), (0, 255, 0))
    converted = _convert_to_rgb(rgb_img)
    assert converted is rgb_img  # Should return original if already RGB

def test_convert_to_rgb_grayscale():
    gray_img = Image.new("L", (10, 10), 128)
    rgb_img = _convert_to_rgb(gray_img)
    assert rgb_img.mode == "RGB"
    assert rgb_img.getpixel((0, 0)) == (128, 128, 128)
